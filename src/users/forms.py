from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordResetForm
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string

from .models import CustomUser
from .tasks import task_send_email
from .services import get_user_by_email
import logging
import pickle

logger = logging.getLogger(__name__)


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email', 'username', 'password1', 'password2', )

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


class CustomPasswordResetForm(PasswordResetForm):
    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        mail_subject = _('Confirm your password reset on ') + context['domain']
        message = render_to_string(
            email_template_name,
            {
                'user': context['user'],
                'protocol': context['protocol'],
                'domain': context['domain'],
                'uid': context['uid'],
                'token': context['token'],
                'site_name': 'Olympiad-helper'
            }
        )
        task_send_email.delay(subject=mail_subject, message=message, to=[to_email])

    def clean_email(self):
        email = self.cleaned_data['email']
        user = get_user_by_email(email)
        if not user:
            raise forms.ValidationError(_('User with inputed email is not exists!'))
        elif not user.is_active:
            raise forms.ValidationError(_('The user is blocked or not confused his mail!'))
        return email


class PasswordResetConfirmForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('password1', 'password2')