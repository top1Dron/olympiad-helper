from django.db import models
from django.utils.translation import ugettext_lazy as _
from judge.models import Problem
from users.models import CustomUser

class Group(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()


    def __str__(self):
        return self.name


class GroupUser(models.Model):
    
    ROLES = (
    # '''enum of user roles in groups'''
    
        ('AD', _('Teacher')),
        ('PP', _('Student')),
    )


    group = models.ForeignKey(to=Group, on_delete=models.CASCADE)
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
    role = models.CharField(max_length=2, choices=ROLES)


class Competition(models.Model):
    title = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()


class CompetitionProblem(models.Model):
    competition = models.ForeignKey(to=Competition, on_delete=models.CASCADE)
    problem = models.ForeignKey(to=Problem, on_delete=models.CASCADE)



class GroupCompetition(models.Model):
    group = models.ForeignKey(to=Group, on_delete=models.CASCADE)
    competition = models.ForeignKey(to=Competition, on_delete=models.CASCADE)
