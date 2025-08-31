from django.db import models


class Loan(models.Model):
    """Model to define loan product templates with their terms and conditions.

        This model stores the basic parameters for different types of loan products
        that can be offered to clients, including interest rates and amount ranges.

        Attributes:
            - id: Auto-incrementing primary key for the loan product.
            - interest: Interest rate as a decimal (e.g., 0.05 for 5%).
            - amount_start: Minimum loan amount that can be borrowed.
            - amount_end: Maximum loan amount that can be borrowed.
            - duration: Loan term duration in months.
            - description: Brief description of the loan product (255 characters max).
        """

    id = models.AutoField(primary_key=True)
    interest = models.FloatField(help_text="Interest rate as a decimal (e.g. 0.05 = 5%)")
    amount_start = models.FloatField(help_text="Minimum loan amount")
    amount_end = models.FloatField(help_text="Maximum loan amount")
    duration = models.IntegerField(help_text="Duration of loan in months")
    description = models.CharField(max_length=255, help_text="Short description of the loan")

    def __str__(self):
        return f"Loan {self.id}: {self.description}\n{self.amount_start} - {self.amount_end} €, {self.interest * 100:.2f}% interest\n Approximate Duration: {self.duration} months"