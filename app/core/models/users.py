from django.db import models

class User(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100, null=False)
    last_name = models.CharField(max_length=100, null=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    password = models.CharField(max_length=100, null=False)
    is_admin = models.BooleanField(null=True, blank=True, default=False)
    is_moderator = models.BooleanField(null=True, blank=True, default=False)
    is_active = models.BooleanField(null=True, blank=True, default=True)