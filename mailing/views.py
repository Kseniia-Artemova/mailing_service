from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
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
    extra_context = {
        'title': 'Создать контакт',
        'button': 'Создать',
    }
    success_url = reverse_lazy('mailing:recipients_list')


class ClientListView(ListView):
    model = Client
    template_name = 'mailing/recipients_list.html'


class ClientUpdateView(UpdateView):
    model = Client
    template_name = 'mailing/recipient_form.html'
    success_url = reverse_lazy('mailing:recipients_list')
    fields = ('name', 'email', 'comment')

    def get_context_data(self, **kwargs) -> dict:
        context_data = super().get_context_data(**kwargs)
        client = Client.objects.get(pk=self.kwargs.get('pk'))
        extra_context = {
            'object': client,
            'title': 'Изменить контакт',
            'button': 'Изменить',
        }
        return context_data | extra_context


class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'mailing/recipient_delete.html'
    success_url = reverse_lazy('mailing:recipients_list')

    def get_context_data(self, **kwargs) -> dict:
        context_data = super().get_context_data(**kwargs)
        context_data['object'] = Client.objects.get(pk=self.kwargs.get('pk'))
        return context_data
