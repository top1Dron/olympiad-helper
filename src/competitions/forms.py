import logging

from competitions.models import Competition
from django import forms
from django.utils.translation import ugettext_lazy as _


logger = logging.getLogger(__name__)


class CompetitionForm(forms.ModelForm):
    title = forms.CharField(label=_('Competition title'), max_length=100)
    start_date = forms.DateTimeField(
        label=_('Competition start date'),
        input_formats=['%d.%m.%Y %H:%M'],
    )
    end_date = forms.DateTimeField(
        label=_('Competition end date'),
        input_formats=['%d.%m.%Y %H:%M'],
    )

    class Meta:
        model = Competition
        fields = ('title', 'start_date', 'end_date', 'description')

    def clean(self):
        data = self.cleaned_data
        if data['end_date'] <= data['start_date']:
            raise forms.ValidationError(_('End date have to go after start_date'))
        return super().clean()