from datetime import timedelta

from django.db import IntegrityError
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.utils import timezone
import requests
import os
import html

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

def llm_generate_reply(message_history: list):
    model_url = os.getenv("LLM_URL")
    model_name = os.getenv("LLM_NAME")

    if not model_url:
        raise EnvironmentError("AI_MODEL_URL environment variable not set")

    headers = {
        "Content-Type": "application/json",
    }

    payload = {
        "model": f"{model_name}",
        "messages": message_history
    }

    response = requests.post(f"{model_url}chat/completions", json=payload, headers=headers)

    if response.status_code == 200:
        result = response.json()
        print("Successful response")
        return result.get("choices")[0].get("message").get("content")
    else:
        raise RuntimeError(f"Model API error: {response.status_code} {response.text}")


def create_chat(credit_offer, user):
    chat = Chat.objects.create(
        credit_offer=credit_offer,
        user=user
    )
    return chat.id

def rephraze_offer(offer):
    """
       Given a CreditOffer ID, returns all relevant relational data
       from CreditOffer, Loan, and Client for context building in an LLM chatbot.
    """
    context_lines = []
    # Add more context if needed
    if offer.loan_type:
        context_lines.append("\nLoan Details:")
        context_lines.append(f"- Interest Rate: {offer.loan_type.interest}")
        context_lines.append(f"- Amount Range: {offer.loan_type.amount_start} to {offer.loan_type.amount_end}")
        context_lines.append(f"- Duration: {offer.loan_type.duration} months")
        context_lines.append(f"- Description: {offer.loan_type.description or 'N/A'}")

    # Client details
    if offer.client:
        context_lines.append("\nClient Details:")
        context_lines.append(f"- Name: {offer.client.user.first_name} {offer.client.user.last_name}")
        context_lines.append(f"- Age: {offer.client.age}")
        context_lines.append(f"- Employed: {offer.client.is_employed}")
        context_lines.append(f"- Salary: {offer.client.salary}")
        context_lines.append(f"- Current Debt: {offer.client.current_debt}")
        context_lines.append(f"- Sex: {offer.client.sex or 'N/A'}")
        context_lines.append(
            f"- Risk Score: {offer.client.risk_score if offer.client.risk_score is not None else 'N/A'}")
        context_lines.append(
            f"- Propensity Score: {offer.client.propensity_score if offer.client.propensity_score is not None else 'N/A'}")

    return "\n".join(context_lines)

def save_messages(chat_id, messages_list):
    messages_redacted = html.unescape(messages_list)
    print(f"Messages redacted: {messages_redacted}, type: {type(messages_redacted)}")
    Chat.objects.filter(id=chat_id).update(message_history=messages_redacted)

