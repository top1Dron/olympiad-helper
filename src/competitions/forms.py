from competitions.models import Competition
from django import forms


class CompetitionForm(forms.ModelForm):
    
    class Meta:
        model = Competition
        fields = ('title', 'start_date', 'end_date')