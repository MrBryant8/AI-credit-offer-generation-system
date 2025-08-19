import ClientManager


def run_pipeline():
    cm = ClientManager()
    new_clients = cm.check_for_new_clients()
    for client in new_clients:
        risk = cm.predict_credit_risk()
        if risk < 0.5:
            cm.generate_offer()


if __name__ == "main":
    run_pipeline()