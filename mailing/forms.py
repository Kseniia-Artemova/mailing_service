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

    start_time = forms.DateTimeField(
        widget=forms.TextInput(attrs={'class': 'datetimepicker'})
    )
    end_time = forms.DateTimeField(
        widget=forms.TextInput(attrs={'class': 'datetimepicker'})
    )
    recipients = forms.ModelMultipleChoiceField(
        queryset=Client.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'select2'})
    )

    class Meta:
        model = Mailing
        exclude = ('status',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'mb-3'


