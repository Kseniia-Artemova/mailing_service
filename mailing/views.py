from django.shortcuts import render
from django.views.generic import CreateView
from mailing.models import Client, Message, Log, Mailing

# Create your views here.


class HomeView(CreateView):
    model = Mailing
    template_name = 'mailing/home.html'
    fields = ('timedate', 'frequency', 'status', 'message')

