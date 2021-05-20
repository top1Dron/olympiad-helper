from django.db import models
from django.utils.translation import ugettext_lazy as _
from groups.models import Group


class Competition(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(verbose_name=_('Description'))
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    group = models.ForeignKey(to=Group, on_delete=models.CASCADE, null=True, default=None, blank=True)


    def __str__(self):
        return self.title


    class Meta:
        ordering = ('id', )
        verbose_name = _('Competition')
        verbose_name_plural = _('Competitions')