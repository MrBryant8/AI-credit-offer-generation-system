from ClientManager import ClientManager


def run_pipeline():
    cm = ClientManager()
    new_clients = cm.check_for_new_clients()
    for client in new_clients:
        low_risk_probability = cm.predict_credit_risk(client)
        if low_risk_probability < 0.25: # Threshold to determine if a client is worth the risk, the lesser, the worse
            continue

        cm.create_offer(client)
        cm.rest.add_risk_score_to_customer(client.get("id"), low_risk_probability)



run_pipeline()