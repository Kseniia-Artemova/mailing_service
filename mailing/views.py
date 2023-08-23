from django.shortcuts import render
from django.views.generic import CreateView
from mailing.models import Client, Message, Log, Mailing

# Create your views here.


class HomeView(CreateView):
    model = Mailing
    template_name = 'mailing/home.html'
    fields = ('recipients', 'timedate', 'frequency', 'message')

    def post(self, request, *args, **kwargs):
        print(request.POST.getlist('recipients'))
        print(request.POST.get('frequency'))
        print(request.POST.get('subject'))
        print(request.POST.get('body'))
        print(request.POST.get('schedule_time'))
        print(request.POST.get('schedule_date'))

        return super().post(request, *args, **kwargs)


class ClientCreateView(CreateView):
    model = Client
    template_name = 'mailing/recipient_form.html'
    fields = ('name', 'email', 'comment')
