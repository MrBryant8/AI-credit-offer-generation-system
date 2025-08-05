from django.db import models
from django.utils import timezone
from .clients import Client
from .loan_types import Loan

class CreditOffer(models.Model):
    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    loan_type = models.ForeignKey(Loan,on_delete=models.PROTECT, null=True, blank=True)
    email_content = models.TextField(unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    moderator_feedback = models.TextField(null=True, blank=True)
    is_draft = models.BooleanField(default=True)
    is_accepted = models.BooleanField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

