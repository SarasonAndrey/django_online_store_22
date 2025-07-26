from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class RegisterForm(UserCreationForm):
    """
    Форма регистрации нового пользователя с email и паролем.
    """

    email = forms.EmailField(
        label="Электронная почта",
        widget=forms.EmailInput(attrs={"placeholder": "example@domain.com"}),
    )

    class Meta:
        model = User
        fields = ("email", "password1", "password2")


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email", "avatar", "phone", "country"]
        labels = {
            "email": "Email",
            "avatar": "Аватар",
            "phone": "Номер телефона",
            "country": "Страна",
        }
