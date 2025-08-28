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
    RISK_THRESHOLD = getattr(settings, "RISK_THRESHOLD")
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


def prepare_chat_list(user_id):
    all_chats = Chat.objects.filter(user_id=user_id).order_by('id')
    return all_chats

def get_high_risk_clients(threshold):
    result = Client.objects.filter(risk_score__lt=threshold).select_related('user').order_by('risk_score')
    return result


def send_email(to_email, subject, email_body, format="plain", encoding="utf-8"):
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@smartcredit.com')
    host_user = getattr(settings, 'EMAIL_HOST_USER')
    host_password = getattr(settings, 'EMAIL_HOST_PASSWORD')
        
    email = MIMEMultipart("alternative")
    email.attach(MIMEText(email_body, format, encoding))
    email["Subject"] = subject
 
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.ehlo()
        connection.starttls()
        connection.login(user=host_user, password=host_password)
        connection.sendmail(
            from_addr=from_email,
            to_addrs=to_email,
            msg=email.as_string())
        

def get_agent_feedback():
    return AgentFeedback.objects.filter(is_reviewed=False).order_by('created_at').first()
    

def redact_email_content(email_content: str):
    """
    Convert email_content markdown to HTML
    """
    if not email_content:
        return ""
    
    import html
    import re
    
    # First, find all blocks containing lines starting with "* "
    def block_replacer(match):
        block = match.group(0)
        # Replace each bullet line with HTML <li>
        items = re.findall(r'^\* (.+)', block, re.MULTILINE)
        lis = ''.join(f'<li>{item}</li>' for item in items)
        return f'<ul>{lis}</ul>'

    escaped_text = html.escape(email_content)
    
    # Step 1: Convert markdown links [text](url) to HTML links
    escaped_text = re.sub(
        r'\[([^\]]+)\]\((https?://[^\)]+)\)', 
        r'<a href="\2">\1</a>', 
        escaped_text
    )
    
    # Step 2: Convert plain URLs to clickable links
    # Match URLs that are not already in <a> tags
    escaped_text = re.sub(
        r'(?<!href=")(?<!href=\')\b(https?://[^\s<>"\']+)',
        r'<a href="\1">\1</a>',
        escaped_text
    )
    
    # Step 3: Convert **bold** to <strong>
    escaped_text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', escaped_text)

    # Step 4: Convert bullet lists
    escaped_text = re.sub(r'(?:^\* .+\n?)+', block_replacer, escaped_text, flags=re.MULTILINE)
    
    # Step 5: Convert numbered lists (1. 2. 3. etc.)
    def numbered_block_replacer(match):
        block = match.group(0)
        # Replace each numbered line with HTML <li>
        items = re.findall(r'^\d+\.\s+(.+)', block, re.MULTILINE)
        lis = ''.join(f'<li>{item}</li>' for item in items)
        return f'<ol>{lis}</ol>'
    
    escaped_text = re.sub(r'(?:^\d+\.\s+.+\n?)+', numbered_block_replacer, escaped_text, flags=re.MULTILINE)
    
    # Step 6: Convert line breaks to <br>
    escaped_text = escaped_text.replace('\\n', '<br>')
    
    return escaped_text
