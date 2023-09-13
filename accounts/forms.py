from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from . import utils
from .models import CustomUser


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.widgets.TextInput(
            attrs={'placeholder': "username", "class": "form-control"})
        self.fields['password'].widget = forms.widgets.PasswordInput(
            attrs={'placeholder': "password", "class": "form-control"})


class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget = forms.widgets.TextInput(
            attrs={'Имя пользователя': "username", "class": "form-control"})
        self.fields['email'].widget = forms.widgets.EmailInput(
            attrs={'Ваш email': "email", "class": "form-control"})
        self.fields['password1'].widget = forms.widgets.PasswordInput(
            attrs={'Ваш пароль': "password", "class": "form-control"})
        self.fields['password2'].widget = forms.widgets.PasswordInput(
            attrs={'Повторите пароль': "repeat password", "class": "form-control"})

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise ValidationError(_("email already exists"))
        return email

    class Meta:
        model = get_user_model()
        fields = ("username", "email")


class ForgetPasswordForm(forms.Form):
    new_password1 = forms.CharField(
        label=_("Новый пароль"),
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                'placeholder': _("New password")
            }
        ),
    )

    new_password2 = forms.CharField(
        label="Повторите пароль",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                'placeholder': _("Confirm password")
            }
        ),
    )

    email = forms.EmailField(
        label='Введите email',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': _("Email")
            }
        ),
    )

    code = forms.CharField(
        label=_('Код подтверждения'),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': _("Code")
            }
        ),
    )

    def clean_new_password2(self):
        password1 = self.data.get("new_password1")
        password2 = self.data.get("new_password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(_("passwords do not match"))
        password_validation.validate_password(password2)

        return password2

    def clean_email(self):
        user_email = self.cleaned_data.get("email")
        if not CustomUser.objects.filter(
                email=user_email
        ).exists():
            raise ValidationError(_("email does not exist"))
        return user_email

    def clean_code(self):
        code = self.cleaned_data.get("code")
        error = utils.verify(
            email=self.cleaned_data.get("email"),
            code=code,
        )
        if error:
            raise ValidationError(error)
        return code


class ForgetPasswordCodeForm(forms.Form):
    email = forms.EmailField(
        label=_('Email'),
    )


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'username',)
