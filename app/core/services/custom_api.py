from datetime import timedelta

from django.db import IntegrityError
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.utils import timezone
import requests, os

from ..models import *

def add_new_user(first_name, last_name, email, password):

    User = get_user_model()

    if User.objects.filter(email=email).exists():
        error_message = "Ein Nutzer mit dieser E-Mail existiert bereits."
        raise IntegrityError(error_message)
    else:
        hashed_password = make_password(password)
        user = User.objects.create(
            email=email,
            password=hashed_password,
            first_name=first_name,
            last_name=last_name,
        )
        Client.objects.create(
            user=user
        )
    return user

def fetch_credit_offers_per_user(user_id):
    deactivate_old_credit_offers()
    credit_offers = CreditOffer.objects.filter(client_id=user_id)
    return credit_offers

def deactivate_old_credit_offers():
    expiry_cutoff = timezone.now() - timedelta(weeks=1)
    CreditOffer.objects.filter(is_active=True, created_at__lt=expiry_cutoff).update(is_active=False)

def LLM_generate_reply(message_history: list):
    model_url = os.getenv("LLM_URL")
    model_name = os.getenv("LLM_NAME")

    if not model_url:
        raise EnvironmentError("AI_MODEL_URL environment variable not set")

    payload = {
        "model": f"{model_name}",
        "messages": message_history
    }

    response = requests.post(f"{model_url}/chat/completions", json=payload)

    if response.status_code == 200:
        result = response.json()
        print(result)
        return result.get("text", "")
    else:
        raise RuntimeError(f"Model API error: {response.status_code} {response.text}")


def create_chat(credit_offer, user):
    chat = Chat.objects.create(
        credit_offer=credit_offer,
        user=user
    )
    return chat.id

    



