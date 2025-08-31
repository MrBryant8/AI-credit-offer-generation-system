import json
import joblib
import pandas as pd
from Client_REST_Interface import REST

class ClientManager:
    """
    Client Manager Class to manage clients, predict risk score and generate offers.
    """
    def __init__(self):
        self.rest=REST()
    
    def check_for_new_clients(self):
        all_clients=self.rest.get_all_customers()
        new_clients= self.get_new_clients(all_clients)
        return new_clients

    def predict_credit_risk(self, client):
        pipeline = joblib.load("ml/output/credit_risk_pipeline.joblib")
        client_df = self.generate_client_dataframe(client)
        low_risk_probability = pipeline.predict_proba(client_df)[0, 1]
        return low_risk_probability


    def generate_client_dataframe(self, client):
        cpm, ag, cac, dc = self.generate_additional_features(client.get("age"), client.get("duration"), client.get("credit_amount"))
        
        df_new = pd.DataFrame([{
            "Age": client.get("age"), 
            "Sex": client.get("sex"),
            "Job": client.get("job"), 
            "Housing": client.get("housing"),
            "Saving accounts": client.get("saving_account"), 
            "Checking account": client.get("checking_account"),
            "Credit amount": client.get("credit_amount"), 
            "Duration": client.get("duration"), 
            "Purpose": client.get("purpose"),
            "Credit_per_month": cpm,
            "Age_group": ag,
            "Credit_amount_category": cac,
            "Duration_category": dc
        }])
        return df_new

    def generate_additional_features(self, client_age, client_loan_duration, client_loan_amount):
        credit_per_month = client_loan_amount / client_loan_duration

        age_group = self.calculate_age_group(client_age)

        credit_amount_category = self.calculate_credit_amount_category(client_loan_amount)

        duration_category = self.calculate_duration_category(client_loan_duration)
        
        return credit_per_month, age_group, credit_amount_category, duration_category

    def create_offer(self, client):

        loan_types = self.rest.get_all_loan_types()
        loan_type = self.determine_loan_type(loan_types, client.get("credit_amount"))
        user_name = self.get_user_name_from_client(client.get("user"))

        details_link = f"http://localhost:8000/my-offers"

        loan_type_desc = "The perfect loan for small buying and a solid ground for something bigger." if not loan_type else loan_type.get("description")
        loan_type_id = 0 if not loan_type else loan_type.get("id")
        email_json = self.rest.generate_email(client, loan_type_desc, user_name, details_link)
        email_dict = json.loads(email_json)
        offer_saved = self.rest.save_offer(client.get("id"), loan_type_id, email_dict["subject"], email_dict["content"])

        if offer_saved:
            print(f"Offer generated for {user_name}")
            return True
        else:
            print(f"Offer couldn't be saved for {user_name}")
            return False

    
    @staticmethod
    def get_new_clients(clients_list_json):
        new_clients = []
        for client in clients_list_json:
            if not client.get("risk_score") and client.get("is_active") is False:
                new_clients.append(client)

        return new_clients

    @staticmethod
    def determine_loan_type(loan_types, amount):
        for loan in loan_types:
            if loan.get("amount_start") <= amount < loan.get("amount_end"):
                return loan
            
    def get_user_name_from_client(self, client_user_id):
        user = self.rest.get_user_by_user_id(client_user_id)
        return f"{user.get("first_name")} {user.get("last_name")}"
    
    def get_next_offer_id(self):
        offers = self.rest.get_all_credit_offers()
        return int(offers[-1].get("id")) + 1
    
    @staticmethod
    def calculate_age_group(age):
        if 0 <= age < 25:
            return "Young"
        elif 25 <= age < 35:
            return "Adult"
        elif 35 <= age <= 50:
            return "Middle_aged"
        else:
            return "Senior"
        
    @staticmethod
    def calculate_credit_amount_category(credit_amount):
        if 0 <= credit_amount < 2000:
            return "Low"
        elif 2000 <= credit_amount < 5000:
            return "Medium"
        elif 5000 <= credit_amount <= 10000:
            return "High"
        else:
            return "Very_high"
        

    @staticmethod
    def calculate_duration_category(duration):
        if 0 <= duration < 12:
            return "Short"
        elif 12 <= duration < 24:
            return "Medium"
        elif 24 <= duration <= 36:
            return "Long"
        else:
            return "Very_long"
    

