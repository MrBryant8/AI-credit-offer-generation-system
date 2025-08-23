from abc import abstractmethod
import joblib
import pandas as pd
from Client_REST_Interface import REST


class ClientManager:
    def __init__(self):
        self.rest=REST()
    
    def check_for_new_clients(self):
        all_clients=self.rest.get_all_customers()
        new_clients= self.get_new_clients(all_clients)
        return new_clients

    def predict_credit_risk(self, client):
        pipeline = joblib.load("ml/output/credit_risk_pipeline.joblib")
        client_df = self.generate_client_dataframe(client)
        is_eligible = True if pipeline.predict_proba(client_df)[0, 1] > 0.5 else False
        return is_eligible

    @staticmethod
    def generate_client_dataframe(client):
        # TODO
        # Prepare a dataframe with the same columns as training AFTER applying the same feature engineering.
        # If feature engineering was done outside the pipeline, ensure to replicate it here before calling predict/predict_proba.
        df_new = pd.DataFrame([{
            "Age": 35, "Sex": "male", "Job": 2, "Housing": "own",
            "Saving accounts": "moderate", "Checking account": "moderate",
            "Credit amount": 3000, "Duration": 18, "Purpose": "car",
            "Credit_per_month": 3000/18,
            "Age_group": "Adult",
            "Credit_amount_category": "Medium",
            "Duration_category": "Medium"
        }])
        return df_new

    @staticmethod
    def generate_additional_features(client_age, client_loan_duration, client_loan_ammount):
        #TODO 
        pass

    def create_offer(self, client):

        loan_types = self.rest.get_all_loan_types()
        loan_type = self.determine_loan_type(loan_types, client.get("credit_amount"))
        user_name = self.get_user_name_from_client(client.get("user"))

        new_offer_id = self.get_next_offer_id()
        details_link = f"http://localhost:8000/offers/{new_offer_id}"

        loan_type_desc = "The perfect loan for small buying and a solid ground for something bigger." if not loan_type else loan_type.get("description")
        loan_type_id = 0 if not loan_type else loan_type.get("id")
        email_json = self.rest.generate_email(client, loan_type_desc, user_name, details_link)

        offer_saved, offer_id = self.rest.save_offer(client.get("id"), loan_type_id, email_json)

        print(new_offer_id, offer_id)
        if offer_saved and offer_id == new_offer_id:
            print(f"Offer generated for {user_name}")
        else:
            print(f"Offer couldn't be saved for {user_name}")

    
    @staticmethod
    def get_new_clients(clients_list_json):
        new_clients = []
        for client in clients_list_json:
            if not client.get("risk_score"):
                new_clients.append(client)

        return new_clients

    @staticmethod
    def determine_loan_type(loan_types, amount):
        for loan in loan_types:
            if loan.get("amount_start") < amount < loan.get("amount_end"):
                return loan
            
    def get_user_name_from_client(self, client_user_id):
        user = self.rest.get_user_by_user_id(client_user_id)
        return f"{user.get("first_name")} {user.get("last_name")}"
    
    def get_next_offer_id(self):
        offers = self.rest.get_all_credit_offers()
        return int(offers[-1].get("id")) + 1
    

