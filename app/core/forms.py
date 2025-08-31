from django import forms
from .models import CreditOffer, Client, User
from django.contrib.auth.forms import PasswordChangeForm

class UserRegisterForm(forms.ModelForm):
    """
    Form, that is used to register a new user.
    """
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password']


class UserLoginForm(forms.Form):
    """
    Form, that is used to log in a user.
    """
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserManageForm(forms.ModelForm):
    """
    Form, that is used to manage a user.
    """
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone_number']

class AddClientForm(forms.ModelForm):
    """
    Form, that is used to add a new client to the database.
    """
    class Meta:
        model = Client
        fields = [
            "identity_number",  # required CharField(max_length=15)
            "age",              # required IntegerField
            "sex",              # CharField with choices
            "job",              # IntegerField with choices
            "housing",          # CharField with choices
            "saving_account",   # CharField with choices
            "checking_account", # CharField with choices
            "credit_amount",    # required IntegerField
            "duration",         # IntegerField (default=12)
            "purpose",          # CharField with choices
        ]


class EditClientForm(forms.ModelForm):
    """
    Form, that is used to edit a client in the database.
    """
    class Meta:
        model = Client
        fields = [
            "age",              # required IntegerField
            "sex",              # CharField with choices
            "job",              # IntegerField with choices
            "housing",          # CharField with choices
            "saving_account",   # CharField with choices
            "checking_account", # CharField with choices
            "credit_amount",    # required IntegerField
            "duration",         # IntegerField (default=12)
            "purpose",          # CharField with choices
        ]



class EditOfferEmailForm(forms.ModelForm):
    """
    Form, that is used to edit an offer email in the database.
    """
    class Meta:
        model = CreditOffer
        fields = ['email_subject', 'email_content', 'moderator_feedback']
        widgets = {
            'email_subject': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'email_content': forms.Textarea(attrs={'rows': 8, 'class': 'form-control'}),
            'moderator_feedback': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }
        labels = {
            'email_subject': 'E-Mail Subject',
            'email_content': 'E-Mail Inhalt',
            'moderator_feedback': 'Moderator Kommentar',
        }


class CustomPasswordChangeForm(PasswordChangeForm):

    """
    Form, that is used to change the password of a user.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Customize old password field
        self.fields['old_password'].widget = forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Type your old password here',
        })
        self.fields['old_password'].label = 'Current Password'
        
        # Customize new password field
        self.fields['new_password1'].widget = forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Type your new password here',
        })
        self.fields['new_password1'].label = 'New Password'
        
        # Customize password confirmation field
        self.fields['new_password2'].widget = forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your new password here',
        })
        self.fields['new_password2'].label = 'Confirm New Password'
        
        # Add help text in German
        self.fields['new_password1'].help_text = '''
        <ul class="small text-muted mt-1">
            <li>A minimum of 8 characters.</li>
            <li>Not numbers only.</li>
            <li>Not too similar to personal data.</li>
            <li>Not used too frequently.</li>
        </ul>
        '''

