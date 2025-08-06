from django import forms
from .models import CreditOffer, Client, User

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password']


class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['age', 'is_employed', 'salary', 'current_debt', 'sex']


class EditOfferEmailForm(forms.ModelForm):
    class Meta:
        model = CreditOffer
        fields = ['email_content', 'moderator_feedback']
        widgets = {
            'email_content': forms.Textarea(attrs={'rows': 8, 'class': 'form-control'}),
            'moderator_feedback': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }
        labels = {
            'email_content': 'E-Mail Inhalt',
            'moderator_feedback': 'Moderator Kommentar',
        }

