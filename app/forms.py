from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm

from .models import Review, User


class LoginForm(forms.Form):
    username = forms.CharField(
        required=True,
        label='Логин'
    )
    password = forms.CharField(
        required=True,
        label='Пароль',
        widget=forms.PasswordInput()
    )


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]


class ReviewForm(forms.ModelForm):
    CHOICES = [(i, i) for i in range(1,6)]
    name = forms.CharField(label="Имя")
    text = forms.CharField(widget=forms.Textarea, label='Содержание')
    points = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)

    class Meta(object):
        model = Review
        exclude = ('id', 'user', 'item', 'date_add')
