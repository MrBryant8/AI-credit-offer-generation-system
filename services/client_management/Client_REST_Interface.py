import requests

class REST:

    def __init__(self, base_app="django", rest_api_suffix="api"):
        self.base_url=f"http://{base_app}:8000"
        self.rest_url=f"{self.base_url}/{rest_api_suffix}"
        self.headers = {
            "Content-Type": "application/json"
        }

    def get_all_customers(self):
        url = f"{self.rest_url}/customers/"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def add_risk_score_to_customer(self, customer_id, new_risk_score):
        url = f"{self.rest_url}/customers/{customer_id}/"
        payload = {"risk_score": new_risk_score}
        response = requests.patch(
            url, 
            headers=self.headers, 
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            print(f"Added new risk_score {new_risk_score} to customer {customer_id}")

    def get_all_credit_offers(self):
        url = f"{self.rest_url}/credit-offers/"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_all_loan_types(self):
        url = f"{self.rest_url}/loans/"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_user_by_user_id(self, user_id):
        url = f"{self.rest_url}/users/{user_id}"
        response = requests.get(url, headers=self.headers)
        return response.json()
    
    def generate_email(self, client, loan_type_description, user_name, details_link):

        url=f"{self.base_url}/create-email/"
        payload = {
            "name": user_name,
            "sex": client.get("sex"),
            "age": client.get("age"),
            "loan_purpose": client.get("purpose"),
            "loan_amount": client.get("credit_amount"),
            "loan_duration": client.get("duration"),
            "loan_description": f"{loan_type_description}",
            "details_link": f"{details_link}"
        }

        headers = self.headers.copy()
        headers["Accept"] = "application/json"

        response = requests.post(url, json=payload, headers=headers, timeout=60)
        return response.text
    
    def save_offer(self, client_type_id, loan_type_id, email_content):
        url = f"{self.rest_url}/credit-offers/"
        payload = {
            "client": client_type_id,
            "loan_type": loan_type_id,
            "email_content": email_content
        }
        response = requests.post(url, json=payload, headers=self.headers, timeout=60)
        return 200 <= response.status_code < 300
