from django.db import models

class Loan(models.Model):
    id = models.AutoField(primary_key=True)
    interest = models.FloatField()
    amount_start = models.FloatField()
    amount_end = models.FloatField()
    duration = models.FloatField()