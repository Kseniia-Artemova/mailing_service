from django import forms
from mailing.models import Client


class ClientForm(forms.ModelForm):
    last_name = forms.CharField()
    first_name = forms.CharField()
    father_name = forms.CharField(required=False)

    class Meta:
        model = Client
        fields = ('email', 'comment')
