from django.db import models

class FeedbackConfig(models.Model):
    id = models.AutoField(primary_key=True)
    feedback = models.TextField(null=False)
    is_reviewed = models.BooleanField(null=False, default=False)
    created_at = models.DateTimeField(auto_now_add=True)