from abc import abstractmethod
import joblib
import pandas as pd
import services.REST_Interface as rest


class ClientManager:
    def __init__(self):
        self.rest=rest()
    
    def check_for_new_clients(self):
        all_clients=self.rest.get_all_customers()
        # filter the ones who don't have a risk score
        new_clients= []
        return new_clients

    def predict_credit_risk(self, client):
        pipeline = joblib.load("ml/output/credit_risk_pipeline.joblib")
        client_df = self.generate_client_dataframe(client)
        is_eligible = True if pipeline.predict_proba(client_df)[0, 1] > 0.5 else False
        return is_eligible

    @abstractmethod
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

    @abstractmethod
    def generate_additional_features(client_age, client_loan_duration, client_loan_ammount):
        pass

    def create_offer(self, client_id):
        # fill up all attributes
        # send to agent to write an email
        # confirm and serialize
        # post request and save
        pass


