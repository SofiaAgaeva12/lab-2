from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class SignupForm(UserCreationForm):
    LetterValidator = RegexValidator(r'^[- а-яА-Я]*$')
    LoginValidator = RegexValidator(r'^[- a-zA-Z]*$')

    first_name = forms.CharField(max_length=120, validators=[LetterValidator], required=True,
                                 help_text='Required. Only cyrillic letters, "-" and " ".',
                                 label='ФИО')
    username = forms.CharField(max_length=30, validators=[LoginValidator], required=True,
                               help_text='Required. Only latin letters and "-".',
                               label='Логин')
    email = forms.EmailField(max_length=120, help_text='Enter a valid email.', required=True,
                             label='Email')
    password1 = forms.CharField(max_length=200, label='Пароль')
    password2 = forms.CharField(max_length=200, label='Повтор пароля')
    agreement = forms.BooleanField(initial=True, help_text='Согласие на обработку персональных данных')

    class Meta:
        model = User
        fields = ('first_name', 'username', 'email', 'password1', 'password2')
