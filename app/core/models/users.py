from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """Custom user model extending Django's AbstractUser with email-based authentication.

        This model replaces the default username authentication with email-based login
        and adds role-based permissions for moderators in the credit system.

        Attributes:
           - username: Disabled - not used in this implementation.
           - id: Auto-incrementing primary key for the user.
           - first_name: User's first name (required, 100 characters max).
           - last_name: User's last name (required, 100 characters max).
           - email: User's email address (unique, used for authentication).
           - phone_number: User's phone number (optional, unique if provided).
           - password: Encrypted user password (required).
           - is_moderator: Whether the user has moderator privileges (default False).
           - is_active: Whether the user account is active (default True).

        Authentication:
            Uses email as the primary authentication field instead of username.
            Required fields for user creation are first_name, last_name, and email.
        """

    username = None

    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100, null=False)
    last_name = models.CharField(max_length=100, null=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=True, blank=True, unique=True)
    password = models.CharField(max_length=100, null=False)
    is_moderator = models.BooleanField(null=True, blank=True, default=False)
    is_active = models.BooleanField(null=True, blank=True, default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']