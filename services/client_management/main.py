from ClientManager import ClientManager


def run_pipeline():
    cm = ClientManager()
    new_clients = cm.check_for_new_clients()
    for client in new_clients:
        risk = cm.predict_credit_risk(client)
        if risk < 0.5:
            cm.create_offer(client)
            break #TODO: remove when not in dev



run_pipeline()