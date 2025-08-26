import requests

class REST:

    def __init__(self, base_app="localhost", rest_api_suffix="api"):
        self.base_url=f"http://{base_app}:8000"
        self.rest_url=f"{self.base_url}/{rest_api_suffix}"
        self.headers = {
            "Content-Type": "application/json"
        }

    def get_all_credit_offers(self):
        url = f"{self.rest_url}/credit-offers/"
        response = requests.get(url, headers=self.headers)
        return response.json()
    
    def remove_moderator_feedback_from_offer(self, offer_id):
        url = f"{self.rest_url}/credit-offers/{offer_id}/"
        payload = {"moderator_feedback": ""}
        response = requests.patch(
            url, 
            headers=self.headers, 
            json=payload,
            timeout=30
        )

        if response.status_code == 200:
            print(f"Removed moderator feedback for {offer_id}")

    def get_agent_config(self):
        url = f"{self.rest_url}/agent-configs/1/"
        response = requests.get(url=url, headers=self.headers)
        return response.json()
    
    def change_agent_config(self, new_description):
        url = f"{self.rest_url}/agent-configs/1/"
        response = requests.put(url=url, headers=self.headers, json={"email_task_description": new_description})
        if 200 <= response.status_code < 300:
            print("Agent Config Changed successfully")
 


        