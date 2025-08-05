# forms.py
from django import forms
from .models import CreditOffer

class UserRegisterForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class EditOfferEmailForm(forms.ModelForm):
    class Meta:
        model = CreditOffer
        fields = ['email_content', 'moderator_feedback']
        widgets = {
            'email_content': forms.Textarea(attrs={'rows': 10, 'class': 'form-control'}),
        }
        labels = {
            'email_content': 'E-Mail Inhalt',
        }
