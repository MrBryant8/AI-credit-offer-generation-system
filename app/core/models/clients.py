from django.db import models
from .users import User

class Client(models.Model):
    class Sex(models.TextChoices):
        MALE = 'male'
        FEMALE = 'female'
        NON_BINARY = 'non-binary'

    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    age = models.IntegerField(null=False, blank=False, default=18)
    is_employed = models.BooleanField(null=False, blank=False, default=False)
    salary = models.IntegerField(null=False, blank=False, default=0)
    current_debt = models.IntegerField(null=False, blank=False, default=0)
    sex = models.CharField(
        max_length=10,
        choices=Sex.choices,
        null=True,
    )
    risk_score = models.IntegerField(null=True, blank=True)
    propensity_score = models.IntegerField(null=True, blank=True)
