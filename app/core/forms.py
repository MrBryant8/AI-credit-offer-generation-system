from django import forms
from .models import CreditOffer, Client, User
from django.contrib.auth.forms import PasswordChangeForm

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password']


class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserManageForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone_number', 'is_active', 'is_moderator']

class AddClientForm(forms.ModelForm):
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Customize old password field
        self.fields['old_password'].widget = forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Aktuelles Passwort eingeben',
        })
        self.fields['old_password'].label = 'Aktuelles Passwort'
        
        # Customize new password field
        self.fields['new_password1'].widget = forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Neues Passwort eingeben',
        })
        self.fields['new_password1'].label = 'Neues Passwort'
        
        # Customize password confirmation field
        self.fields['new_password2'].widget = forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Neues Passwort bestätigen',
        })
        self.fields['new_password2'].label = 'Passwort bestätigen'
        
        # Add help text in German
        self.fields['new_password1'].help_text = '''
        <ul class="small text-muted mt-1">
            <li>Mindestens 8 Zeichen lang</li>
            <li>Nicht nur aus Zahlen bestehen</li>
            <li>Nicht zu ähnlich zu Ihren persönlichen Daten</li>
            <li>Nicht zu häufig verwendet werden</li>
        </ul>
        '''

