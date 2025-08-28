from ClientManager import ClientManager
import os

RISK_THRESHOLD = float(os.environ.get("RISK_THRESHOLD", 0.25))
def run_pipeline():
    cm = ClientManager()
    new_clients = cm.check_for_new_clients()
    for client in new_clients:
        low_risk_probability = cm.predict_credit_risk(client)
        if low_risk_probability < RISK_THRESHOLD: # Threshold to determine if a client is worth the risk, the lesser, the worse
            cm.rest.add_risk_score_to_customer(client.get("id"), low_risk_probability)
            continue

        offer_created = cm.create_offer(client)
        if offer_created:
            cm.rest.add_risk_score_to_customer(client.get("id"), low_risk_probability)



run_pipeline()