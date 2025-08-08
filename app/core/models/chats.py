from django.db import models
from .offers import CreditOffer
from .users import User

class Chat(models.Model):
    id = models.AutoField(primary_key=True)
    time_ended = models.DateTimeField(auto_now=True)
    credit_offer = models.ForeignKey(CreditOffer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)