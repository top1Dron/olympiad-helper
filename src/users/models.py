from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
import judge.models as judge_models

from .managers import CustomUserManager

class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


    def get_quantity_of_submissions(self):
        return judge_models.Solution.objects.filter(user=self).count()


    def get_quantity_of_accepted_submissions(self):
        return judge_models.Solution.objects.filter(user=self).filter(status='AC').count()

    def get_quantity_of_solved_problems(self):
        return judge_models.UserProblemStatus.objects.filter(user=self, status='AC').count()


    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

        