from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class JudgeConfig(AppConfig):
    name = 'judge'

    class Meta:
        verbose_name = _('Judge')
