from competitions.models import Competition
from django import forms
from django.utils.translation import ugettext_lazy as _


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