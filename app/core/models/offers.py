from django.db import models
from .clients import Client

class CreditOffer(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Client, on_delete=models.CASCADE)
    amount_offered = models.IntegerField()
    email_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    moderator_feedback = models.TextField()
    is_accepted = models.BooleanField()
    is_active = models.BooleanField()

