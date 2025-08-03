from django.db import IntegrityError
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
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
    credit_offers = CreditOffer.objects.filter(client_id=user_id)
    return credit_offers


