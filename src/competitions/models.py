from django.db import models
from groups.models import Group


class Competition(models.Model):
    title = models.CharField(max_length=100, unique=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    group = models.ForeignKey(to=Group, on_delete=models.CASCADE, null=True, default=None, blank=True)


    def __str__(self):
        return self.title