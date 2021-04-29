from django.db import models
from django.shortcuts import reverse
from django.utils.translation import ugettext_lazy as _
from users.models import CustomUser


class Group(models.Model):
    name = models.CharField(verbose_name=_('Group name'), max_length=50)
    description = models.TextField(verbose_name=_('Group description'))


    def __str__(self):
        return self.name


    class Meta:
        verbose_name = _('Group')
        verbose_name_plural = _('Groups')


class GroupUser(models.Model):
    
    ROLES = (
    # '''enum of user roles in groups'''
    
        ('TE', _('Teacher')),
        ('SD', _('Student')),
    )


    group = models.ForeignKey(to=Group, on_delete=models.CASCADE)
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
    role = models.CharField(verbose_name=_('Role'), max_length=2, choices=ROLES)


    class Meta:
        unique_together = ('group', 'user')


    @property
    def get_delete_url(self):
        return reverse('groups:delete_user_from_group', kwargs={'group_id': self.group.pk, 'group_user_id':self.pk})
