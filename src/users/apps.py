from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class UsersConfig(AppConfig):
    name = 'users'

    class Meta:
        verbose_name = _'Users'
