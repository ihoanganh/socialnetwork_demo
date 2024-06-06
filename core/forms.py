from django import forms
from .models import Group, User, GroupChat


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'decription', 'visibility']


class GroupChatForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        queryset=User.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = GroupChat
        fields = ['name', 'description', 'members']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(GroupChatForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['members'].queryset = user.profile.friends.all()