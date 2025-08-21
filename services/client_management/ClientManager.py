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
        pass

    def create_offer(self, client_id, amount_requested):

        loan_types = self.rest.get_all_loan_types()
        loan_type_id = self.determine_loan_type(loan_types, amount_requested)

        print(f"Offer generated for {client_id}")

    
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
            if loan.amount_start < amount < loan.amount_end:
                return loan.id


