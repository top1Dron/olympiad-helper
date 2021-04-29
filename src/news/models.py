from django.db import models
from django.utils.translation import ugettext_lazy as _


class Article(models.Model):
    title = models.CharField(max_length=120, verbose_name=_('Title'))
    body = models.TextField(verbose_name=_('Body'))
    publication_date = models.DateTimeField(auto_now=True, verbose_name=_('Publication date'))


    def __str__(self):
        return self.title


    class Meta:
        verbose_name = _('Article')
        verbose_name_plural = _('Articles')
        ordering = ('-publication_date', )
        unique_together = ('title', 'publication_date')
        get_latest_by = 'publication_date'
    