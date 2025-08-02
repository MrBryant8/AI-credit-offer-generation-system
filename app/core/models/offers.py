from django.db import models
from django.utils import timezone
from .clients import Client
from .loan_types import Loan

class CreditOffer(models.Model):
    id = models.AutoField(primary_key=True)
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE)
    loan_type_id = models.ForeignKey(Loan, on_delete=models.CASCADE, default=1)
    email_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    moderator_feedback = models.TextField()
    is_accepted = models.BooleanField()
    is_active = models.BooleanField()
    expires_at = models.DateTimeField(default=timezone.now)

