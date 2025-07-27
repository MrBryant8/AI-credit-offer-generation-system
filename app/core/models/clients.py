from django.db import models

class Client(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100, null=False)
    last_name = models.CharField(max_length=100, null=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    is_employed = models.BooleanField(null=True, blank=True)
    salary = models.IntegerField()
    current_debt = models.IntegerField()
