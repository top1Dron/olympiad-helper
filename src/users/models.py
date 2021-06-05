from datetime import datetime as dt
from pathlib import Path
import os

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

import judge.models as judge_models
from .managers import CustomUserManager

def get_upload_path(instance, filename):
    return Path('uploads') / dt.now().strftime('%Y/%m-%d') / filename

class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    avatar = models.ImageField(upload_to=get_upload_path, null=True, blank=True)

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


image_attributes = ('avatar',)


@receiver(models.signals.post_delete, sender=CustomUser)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding sender object is deleted.
    """
    for attribute in image_attributes:
        if hasattr(instance, attribute):
            attr = getattr(instance, attribute)
            if attr:
                try:
                    if os.path.isfile(attr.path):
                        os.remove(attr.path)
                except ValueError:
                    pass


@receiver(models.signals.pre_save, sender=CustomUser)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding sender object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        sender_obj = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return False
    for attribute in image_attributes:
        if hasattr(sender_obj, attribute):
            old_file = getattr(sender_obj, attribute)
        if hasattr(instance, attribute):
            new_file = getattr(instance, attribute)

    if not old_file == new_file:
        try:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)
        except ValueError as e:
            pass

        