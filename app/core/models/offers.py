from django.db import models
from django.utils import timezone
from .clients import Client
from .loan_types import Loan

class CreditOffer(models.Model):
    """Model to store credit offers generated for clients based on their profiles.

        This model represents personalized loan offers created for clients, including
        email content, approval workflow status, and moderator feedback for quality control.

        Attributes:
            - id: Auto-incrementing primary key for the credit offer.
            - client: Foreign key reference to the Client receiving this offer.
            - loan_type: Foreign key reference to the Loan product template (optional).
            - email_content: Generated email content for the offer (must be unique).
            - email_subject: Subject line for the offer email.
            - created_at: Timestamp when the offer was first created.
            - updated_at: Timestamp when the offer was last modified.
            - moderator_feedback: Comments from moderators reviewing the offer.
            - is_draft: Whether the offer is still in draft status (default True).
            - is_accepted: Whether the client accepted the offer (null until decided).
            - is_active: Whether the offer is currently active.
        """

    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    loan_type = models.ForeignKey(Loan,on_delete=models.PROTECT, null=True, blank=True)
    email_content = models.TextField(unique=True, null=True, blank=True)
    email_subject = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    moderator_feedback = models.TextField(null=True, blank=True, default="")
    is_draft = models.BooleanField(default=True)
    is_accepted = models.BooleanField(null=True, blank=True)
    is_active = models.BooleanField(default=False)

