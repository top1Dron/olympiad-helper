from django import forms
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
from .models import ProgrammingLanguage, Problem


class LanguageForm(forms.ModelForm):
    name = forms.ModelChoiceField(label=_('Programming language'), widget=forms.Select, queryset=ProgrammingLanguage.objects.all(), empty_label='----')

    class Meta:
        model = ProgrammingLanguage
        fields = ('name',)


class SubmitSolutionForm(forms.Form):
    problem_number = forms.CharField(label=_('Problem number'), max_length=1000)
    programming_language = forms.ModelChoiceField(label=_('Programming language'), widget=forms.Select, queryset=ProgrammingLanguage.objects.all(), empty_label='----')
    source_code = forms.CharField(
        max_length=1000000,
        widget=forms.Textarea(),
        label=_('Source code'),
    )


    def __init__(self, *args, **kwargs):
        super(SubmitSolutionForm, self).__init__(*args, **kwargs)
        self.fields['problem_number'].error_messages = {'required': _('You have to write problem number!')}
        self.fields['programming_language'].error_messages = {'required': _('You have to choose programming language!')}
        self.fields['source_code'].error_messages = {'required': _('You have to put your code! Solution can not be passed without it!')}


class ProblemSearchForm(forms.Form):
    problem_search_field = forms.CharField(
        label=_('Search problem'), 
        max_length=1000, 
        required=False, 
        widget=forms.widgets.Input(attrs={
            'placeholder': _('Type a problem'),
            'name': 'search_problem',
            'type': 'text',
        })
    )

    def __init__(self, *args, **kwargs):
        competition_id = kwargs.get('competition_id')
        if competition_id != None:
            kwargs.pop('competition_id')
        super().__init__(*args, **kwargs)
        if competition_id != None:
            self.fields['problem_search_field'].widget.attrs.update({'problems':reverse_lazy('competitions:search_problem', kwargs={'pk':competition_id})})


class ProblemFilterForm(forms.ModelForm):
    difficulty_choices = list(Problem.DIFFICULTY)
    difficulty_choices.insert(0, ('', _('All problems')))
    difficulty = forms.ChoiceField(choices=tuple(difficulty_choices), label=_('Complexity'))
    
    classification_choices = list(Problem.CLASSIFICATION)
    classification_choices.insert(0, ('', _('All problems')))
    classification = forms.ChoiceField(choices=tuple(classification_choices), label=_('Classification'))

    class Meta:
        model = Problem
        fields = ['number', 'difficulty', 'classification']

    def __init__(self, *args, **kwargs):
        super(ProblemFilterForm, self).__init__(*args, **kwargs)
        self.fields['number'].label = _('Number')
