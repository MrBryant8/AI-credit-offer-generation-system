from django.db import models
from .users import User

class Client(models.Model):
    """Model to store client information for credit risk assessment.

        This model contains personal, financial, and credit-related information
        used to evaluate loan applications and calculate risk scores.

        Attributes:
            - id: Auto-incrementing primary key for the client.
            - user: One-to-one relationship with User model (optional).
            - identity_number: Unique identifier for the client (15 characters max).
            - age: Client's age in years (minimum 18).
            - sex: Client's gender (male/female).
            - job: Employment skill level from jobless to high-skill.
            - housing: Housing situation (own/rent/free).
            - saving_account: Savings account balance category.
            - checking_account: Checking account balance category.
            - credit_amount: Requested loan amount.
            - duration: Loan duration in months (default 12).
            - purpose: Purpose of the loan (car, education, business, etc.).
            - risk_score: Calculated credit risk score (optional).
            - is_active: Whether the client record is currently active.
        """

    class Job(models.IntegerChoices):
        JOBLESS = 0, "jobless"
        LOW_SKILL = 1, "low_skill"
        MEDIUM_SKILL = 2, "medium_skill"
        HIGH_SKILL = 3, "high_skill"

    class Sex(models.TextChoices):
        MALE = 'male'
        FEMALE = 'female'

    class Housing(models.TextChoices):
        OWN = 'own'
        RENT = 'rent'
        FREE = 'free'

    class SavingsAccount(models.TextChoices):
        UNKNOWN = "unknown"
        LITTLE = "little"
        MODERATE = "moderate"
        RICH = "rich"
        QUITE_RICH = "quite rich"

    class CheckingAccount(models.TextChoices):
        UNKNOWN = "unknown"
        LITTLE = "little"
        MODERATE = "moderate"
        RICH = "rich"

    class Purpose(models.TextChoices):
        CAR = "car"
        FURNITURE_OR_EQUIPMENT = "furniture/equipment"
        RADIO_OR_TV = "radio/TV"
        DOMESTIC_APPLIANCES = "domestic appliances"
        REPAIRS = "repairs"
        EDUCATION = "education"
        BUSINESS = "business"
        VACATION_OR_OTHERS = "vacation/others"

    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    identity_number = models.CharField(max_length=15, null=False, unique=True)
    age = models.IntegerField(null=False, blank=False, default=18)
    sex = models.CharField(max_length=10, choices=Sex.choices, null=True)
    job = models.IntegerField(null=False, blank=False, choices=[(j.value, j.name.title()) for j in Job])
    housing = models.CharField(max_length=5, choices=Housing.choices, null=False)
    saving_account = models.CharField(max_length=20, choices=SavingsAccount.choices, null=False)
    checking_account = models.CharField(max_length=20, choices=CheckingAccount.choices, null=False)
    credit_amount = models.IntegerField(null=False, blank=False)
    duration = models.IntegerField(null=False, blank=False, default=12)
    purpose = models.CharField(max_length=100, null=False, choices=Purpose.choices)
    risk_score = models.FloatField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
