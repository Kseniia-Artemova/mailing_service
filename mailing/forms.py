from django import forms
from django.forms import DateTimeInput

from mailing.models import Client, Message, Mailing


class StyleFormMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ClientForm(forms.ModelForm):

    last_name = forms.CharField()
    first_name = forms.CharField()
    father_name = forms.CharField(required=False)

    class Meta:
        model = Client
        fields = ('email', 'comment')


class MessageForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Message
        fields = '__all__'
        labels = {
            'subject': 'Тема',
            'body': 'Тело письма',
        }
        widgets = {
            'body': forms.Textarea(attrs={'rows': 3}),
        }


class MailingForm(StyleFormMixin, forms.ModelForm):

    start_time = forms.DateTimeField(
        label='Время начала',
        widget=DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'})
    )
    end_time = forms.DateTimeField(
        label='Время окончания',
        widget=DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'})
    )
    recipients = forms.ModelMultipleChoiceField(
        label='Получатели',
        queryset=Client.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'select2'})
    )

    class Meta:
        model = Mailing
        exclude = ('status', 'message')


