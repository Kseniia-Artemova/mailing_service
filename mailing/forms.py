from django import forms
from mailing.models import Client, Message, Mailing


class ClientForm(forms.ModelForm):

    last_name = forms.CharField()
    first_name = forms.CharField()
    father_name = forms.CharField(required=False)

    class Meta:
        model = Client
        fields = ('email', 'comment')


class MessageForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = '__all__'


class MailingForm(forms.ModelForm):

    class Meta:
        model = Mailing
        exclude = ('status',)
