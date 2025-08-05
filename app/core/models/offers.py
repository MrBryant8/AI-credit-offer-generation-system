from django.db import models
from django.utils import timezone
from .clients import Client
from .loan_types import Loan

class CreditOffer(models.Model):
    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    loan_type = models.ForeignKey(Loan,on_delete=models.PROTECT)
    email_content = models.TextField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    moderator_feedback = models.TextField()
    is_accepted = models.BooleanField()
    is_active = models.BooleanField(default=True)
    expires_at = models.DateTimeField(default=timezone.now)

