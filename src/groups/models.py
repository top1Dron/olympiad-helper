from django.db import models
from django.utils.translation import ugettext_lazy as _
from users.models import CustomUser


class Group(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()


    def __str__(self):
        return self.name


class GroupUser(models.Model):
    
    ROLES = (
    # '''enum of user roles in groups'''
    
        ('TE', _('Teacher')),
        ('SD', _('Student')),
    )


    group = models.ForeignKey(to=Group, on_delete=models.CASCADE)
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
    role = models.CharField(max_length=2, choices=ROLES)
