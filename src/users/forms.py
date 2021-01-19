from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.core.validators import EmailValidator

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email', 'username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.pop("autofocus", None)


class LoginForm(forms.Form):
    email = forms.CharField(label=_('Email'), max_length=200, required=True, widget=forms.EmailInput())
    password = forms.CharField(label=_('Password'), max_length=100, required=True, widget=forms.PasswordInput())


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email',)


class PasswordResetForm(forms.Form):
    email = forms.CharField(label=_('Email'), max_length=200, required=True, widget=forms.EmailInput())


class PasswordResetConfirmForm(UserCreationForm):
    

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('password1', 'password2')