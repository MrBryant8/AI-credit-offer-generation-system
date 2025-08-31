from django.db import models
from .offers import CreditOffer
from .users import User


class Chat(models.Model):
    """Model to store chat sessions between users and the system chatbot.

    Attributes:
        - id: Auto-incrementing primary key for the chat session.
        - time_ended: Timestamp when the chat session ended (auto-updated).
        - credit_offer: Foreign key reference to the associated CreditOffer.
        - user: Foreign key reference to the User who participated in the chat.
        - message_history: Text field storing the complete chat conversation history.
    """
    id = models.AutoField(primary_key=True)
    time_ended = models.DateTimeField(auto_now=True)
    credit_offer = models.ForeignKey(CreditOffer, on_delete=models.CASCADE, default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    message_history = models.TextField(default="")