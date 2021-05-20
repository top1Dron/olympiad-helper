from django import forms
from groups.models import Group, GroupUser


class GroupForm(forms.ModelForm):

    class Meta:
        model = Group
        fields = ('name', 'description')

class GroupUserForm(forms.ModelForm):
    class Meta:
        model = GroupUser
        fields = ("role", 'user')

    def __init__(self, *args, **kwargs):
        super(GroupUserForm, self).__init__(*args, **kwargs)
        self.fields['role'].choices = self.fields['role'].choices[1:]