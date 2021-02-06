from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import ProgrammingLanguage, Problem


class LanguageForm(forms.ModelForm):
    name = forms.ModelChoiceField(label=_('Programming language'), widget=forms.Select, queryset=ProgrammingLanguage.objects.all(), empty_label='----')

    class Meta:
        model = ProgrammingLanguage
        fields = ('name',)


class SubmitSolutionForm(forms.Form):
    problem_number = forms.CharField(label=_('Problem number'), max_length=10)
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


    # def clean(self):
    #     cleaned_data = super(SubmitSolutionForm, self).clean()
    #     problem_number = cleaned_data.get('problem_number')
    #     programming_language = cleaned_data.get('programming_language')
    #     source_code = cleaned_data.get('source_code')
    #     if not problem_number:
    #         raise forms.ValidationError(_('You have to write problem number!'))
    #     if not programming_language:
    #         raise forms.ValidationError(_('You have to choose programming language!'))
    #     if not source_code:
    #         raise forms.ValidationError(_('You have to put your code! Solution can not be passed without it!'))
 
 
# class TextForm(forms.ModelForm):
#     class Meta:
#         model = Text
#         fields = ('text',)
#         labels = {'Введите код на C++': 'text',}
 
 
# class CodeFileForm(forms.ModelForm):
#     class Meta:
#         model = CodeFile
#         fields = ('file',)
#         labels = {'Завантажте файл': 'file',}