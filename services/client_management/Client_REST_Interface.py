import requests

class REST:

    def __init__(self, base_app="django", api_suffix="api"):
        self.url=f"http://{base_app}:8000/{api_suffix}/"
        self.headers = {
            "Content-Type": "application/json"
        }

    def get_all_customers(self):
        url = f"{self.url}customers/"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_customer_by_id(self, id):
        url = f"{self.url}customers/{id}/"
        response = requests.get(url, headers=self.headers)
        print(response)

    def add_risk_score_to_customer(self, customer_id, new_risk_score):
        url = f"{self.url}customers/{customer_id}/"
        response = requests.patch(url, headers=self.headers, json={"risk_score": new_risk_score})
        print(response)

    def get_all_credit_offers(self):
        url = f"{self.url}credit-offers/"
        response = requests.get(url, headers=self.headers)
        print(response)

        