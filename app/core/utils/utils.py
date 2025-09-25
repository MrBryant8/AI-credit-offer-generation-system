from datetime import timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

from django.db import IntegrityError
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.conf import settings
import requests
import os
import html
import markdown

from ..models import *


def add_new_user(first_name, last_name, email, password):
    """
    Adds a new user + client to the database.
    """
    User = get_user_model()

    if User.objects.filter(email=email).exists():
        error_message = "A user with that email already exists."
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
    client_id = Client.objects.filter(user_id=user_id).first().id
    credit_offers = CreditOffer.objects.filter(client_id=client_id)
    return credit_offers


def deactivate_old_credit_offers():
    """
    Deactivates credit offers, which are older than 1 week.
    """
    expiry_cutoff = timezone.now() - timedelta(weeks=1)
    CreditOffer.objects.filter(is_active=True, created_at__lt=expiry_cutoff).update(is_active=False)


def llm_generate_reply(message_history: list):

    """
    Utils function to handle LLM calls and chat integrity.
    """
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
       Given a CreditOffer, returns all relevant data
       from CreditOffer, Loan, and Client for context building in an LLM chatbot.
    """
    RISK_THRESHOLD = getattr(settings, "RISK_THRESHOLD")
    context_lines = []
   
    if offer.loan_type:
        context_lines.append("\nLoan Details:")
        context_lines.append(f"- Interest Rate: {offer.loan_type.interest  * 100}")
        context_lines.append(f"- Amount Range: {offer.loan_type.amount_start} to {offer.loan_type.amount_end}")
        context_lines.append(f"- Duration: {offer.loan_type.duration} months")
        context_lines.append(f"- Description: {offer.loan_type.description or 'N/A'}")

    if offer.client:
        context_lines.append("\nClient Details:")
        context_lines.append(f"- Name: {offer.client.user.first_name} {offer.client.user.last_name}")
        context_lines.append(f"- Age: {offer.client.age}")
        context_lines.append(f"- Sex: {offer.client.sex}")
        context_lines.append(f"- Job Skill Level: {offer.client.job}")
        context_lines.append(f"- Housing: {offer.client.housing}")
        context_lines.append(f"- Saving Account Status: {offer.client.saving_account}")
        context_lines.append(f"- Checking Account Status: {offer.client.checking_account}")
        context_lines.append(f"- Loan Amount Requested: {offer.client.credit_amount}")
        context_lines.append(f"- Loan Repayment duration: {offer.client.duration}")
        context_lines.append(f"- Loan Purpose: {offer.client.purpose}")
        context_lines.append(f"- Is offer active? {"Yes" if offer.is_active else "No"}")
        context_lines.append(
            f"- Loan Approved: {"Approved" if offer.client.risk_score and offer.client.risk_score > RISK_THRESHOLD  else "Denied"}")
        
    return "\n".join(context_lines)


def save_messages(chat_id, messages_list):
    """
    Save messages in JSON.
    """
    messages_redacted = html.unescape(messages_list)
    messages_redacted_json =(messages_redacted.
                             replace("'role'", '"role"')
                             .replace("'content'", '"content"')
                             .replace("'user'", '"user"')
                             .replace("'assistant'", '"assistant"')
                             .replace("'system'", '"system"')
                             .replace(": '", ': "')
                             .replace("'}", '"}')
                             .replace('"', '\"')
                             .replace('\n', '\\n')
                             .replace('\r', '\\r')
                             .replace('\t', '\\t'))

    Chat.objects.filter(id=chat_id).update(message_history=messages_redacted_json)


def prepare_chat_list(user_id, offer_id):
    all_chats = Chat.objects.filter(user_id=user_id, credit_offer_id=offer_id).order_by('id')
    return all_chats

def get_high_risk_clients(threshold):
    result = Client.objects.filter(risk_score__lt=threshold).select_related('user').order_by('risk_score')
    return result


def send_email(receiver_email, subject, email_body, format="plain", encoding="utf-8"):

    """
    Function to send offers to users via E-Mail ( SMTP ).
    """
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@smartcredit.com')
    host_user = getattr(settings, 'EMAIL_HOST_USER')
    host_password = getattr(settings, 'EMAIL_HOST_PASSWORD')
    to_email_list = [getattr(settings, 'DEFAULT_EMAIL_RECEIVER')]
    if not receiver_email.endswith("@smartcredit.com"):
        to_email_list.append(receiver_email)

    email = MIMEMultipart("alternative")
    email.attach(MIMEText(email_body, format, encoding))
    email["Subject"] = subject
 
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.ehlo()
        connection.starttls()
        connection.login(user=host_user, password=host_password)
        connection.sendmail(
            from_addr=from_email,
            to_addrs=to_email_list,
            msg=email.as_string())
        

def get_agent_feedback():
    return AgentFeedback.objects.filter(is_reviewed=False).order_by('created_at').first()
    

def redact_markdown_content(email_content: str):
    """
    Convert email_content markdown to HTML
    """
    if not email_content:
        return ""
    
    return markdown.markdown(email_content)
