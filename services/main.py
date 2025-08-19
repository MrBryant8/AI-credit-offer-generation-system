import ClientManager
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:admin@pgdb:5432/")

def run_pipeline():
    cm = ClientManager(DATABASE_URL)
    new_clients = cm.check_for_new_clients()
    pass

if __name__ == "main":
    run_pipeline()