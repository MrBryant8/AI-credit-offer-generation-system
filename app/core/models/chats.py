from django.db import models

class Chat(models.Model):
    id = models.AutoField(primary_key=True)
    time_started = models.DateTimeField(auto_now_add=True)
    time_ended = models.DateTimeField(auto_now=True)