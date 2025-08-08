from django.db import models
from .users import User
from .chats import Chat

class Message(models.Model):
    id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    chats = models.ForeignKey(Chat, on_delete=models.CASCADE, default=0)
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
