from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class SignupForm(UserCreationForm):
    LetterValidator = RegexValidator(r'^[- а-яА-Я]*$')
    LoginValidator = RegexValidator(r'^[- a-zA-Z]*$')
    username = forms.CharField(max_length=120, required=True, help_text='Enter a short name in English')
    fullname = forms.CharField(max_length=120, validators=[LetterValidator], required=True,
                               help_text='Required. Only cyrillic letters, "-" and " ".')
    email = forms.EmailField(max_length=120, help_text='Enter a valid email.', required=True,)
    login = forms.CharField(max_length=30, validators=[LoginValidator], required=True,
                            help_text='Required. Only latin letters and "-".')
    agreement = forms.BooleanField(initial=True, help_text='Consent to the processing of personal data')

    class Meta:
        model = User
        fields = ('username', 'fullname', 'login', 'email', 'password1', 'password2')
