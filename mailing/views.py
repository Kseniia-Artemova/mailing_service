from django.forms import inlineformset_factory
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from mailing.forms import ClientForm, MailingForm, MessageForm
from mailing.models import Client, Message, Log, Mailing

# Create your views here.


class HomeView(CreateView):
    model = Mailing
    template_name = 'mailing/home.html'
    form_class = MailingForm

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        VersionFormset = inlineformset_factory(Message, Mailing, form=MailingForm, extra=1, can_delete=False)
        if self.request.method == 'POST':
            formset = VersionFormset(self.request.POST, instance=self.object)
        else:
            formset = VersionFormset(instance=self.object)

        context_data['object_list'] = Client.objects.order_by('name')
        context_data['formset'] = formset

        return context_data


class ClientCreateView(CreateView):
    model = Client
    template_name = 'mailing/recipient_form.html'
    form_class = ClientForm
    success_url = reverse_lazy('mailing:recipients_list')
    extra_context = {
        'title': 'Создать контакт',
        'button': 'Создать',
    }

    def form_valid(self, form):
        last_name = form.cleaned_data.get('last_name').strip()
        first_name = form.cleaned_data.get('first_name').strip()
        father_name = form.cleaned_data.get('father_name', '').strip()

        full_name = f"{last_name} {first_name} {father_name}".strip().title()

        form.instance.name = full_name

        return super().form_valid(form)


class ClientListView(ListView):
    model = Client
    template_name = 'mailing/recipients_list.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['object_list'] = Client.objects.order_by('-changing_data')
        return context_data


class ClientUpdateView(UpdateView):
    model = Client
    template_name = 'mailing/recipient_form.html'
    success_url = reverse_lazy('mailing:recipients_list')
    form_class = ClientForm

    def get_context_data(self, **kwargs) -> dict:
        context_data = super().get_context_data(**kwargs)
        extra_context = {
            'object': Client.objects.get(pk=self.kwargs.get('pk')),
            'title': 'Изменить контакт',
            'button': 'Сохранить',
        }
        return context_data | extra_context

    def form_valid(self, form):
        last_name = form.cleaned_data.get('last_name').strip()
        first_name = form.cleaned_data.get('first_name').strip()
        father_name = form.cleaned_data.get('father_name', '').strip()

        full_name = f"{last_name} {first_name} {father_name}".strip().title()

        form.instance.name = full_name
        print(form.instance.id)
        print(self.request.method)

        return super().form_valid(form)


class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'mailing/recipient_delete.html'
    success_url = reverse_lazy('mailing:recipients_list')

    def get_context_data(self, **kwargs) -> dict:
        context_data = super().get_context_data(**kwargs)
        context_data['object'] = Client.objects.get(pk=self.kwargs.get('pk'))
        return context_data


class MailingListView(ListView):
    model = Mailing
    template_name = 'mailing/mailing_list.html'


class MailingCreateView(CreateView):
    model = Mailing
    template_name = 'mailing/mailing_form.html'
    fields = ('recipients', 'start_time', 'end_time', 'frequency', 'message')
    success_url = reverse_lazy('mailing:mailing_list')
    extra_context = {
        'object_list': Client.objects.order_by('name'),
        'title': 'Создать рассылку',
        'button': 'Создать',
    }


class MailingUpdateView(UpdateView):
    model = Mailing
    template_name = 'mailing/mailing_form.html'
    fields = ('recipients', 'start_time', 'end_time', 'frequency', 'message')
    success_url = reverse_lazy('mailing:mailing_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mailing = self.get_object()
        context['title'] = 'Изменить рассылку'
        context['button'] = 'Сохранить'
        context['mailing'] = mailing
        context['mailing_schedule_date'] = mailing.timedate.strftime('%Y-%m-%d')
        context['mailing_schedule_time'] = mailing.timedate.strftime('%H:%M')
        print(context['mailing_schedule_date'])
        print(context['mailing_schedule_time'])
        context['object_list'] = Client.objects.all()
        context['recipient_ids'] = list(mailing.recipients.values_list('id', flat=True))
        return context


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = 'mailing/mailing_delete.html'
    success_url = reverse_lazy('mailing:mailing_list')

    def get_context_data(self, **kwargs) -> dict:
        context_data = super().get_context_data(**kwargs)
        context_data['object'] = Mailing.objects.get(pk=self.kwargs.get('pk'))
        return context_data
