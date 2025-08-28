from django.db import models


#TODO: update with more relevant values
class Loan(models.Model):
    id = models.AutoField(primary_key=True)
    interest = models.FloatField(help_text="Interest rate as a decimal (e.g. 0.05 = 5%)")
    amount_start = models.FloatField(help_text="Minimum loan amount")
    amount_end = models.FloatField(help_text="Maximum loan amount")
    duration = models.IntegerField(help_text="Duration of loan in months")
    description = models.CharField(max_length=255, help_text="Short description of the loan")

    def __str__(self):
        return f"Loan {self.id}: {self.description}\n{self.amount_start} - {self.amount_end} €, {self.interest * 100:.2f}% interest\n Approximate Duration: {self.duration} months"