from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, BaseUserCreationForm
from .models import CustomUser


class CustomUserCreationForm(BaseUserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'username', 'password1', 'password2')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'username',)
