from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.forms import inlineformset_factory
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView

from blog.models import BlogEntry
from mailing.forms import ClientForm, MailingForm, MessageForm
from mailing.models import Client, Message, Log, Mailing

# Create your views here.


class MailingAndMessageSaveMixin:

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        if self.request.POST:
            context_data['message_form'] = MessageForm(self.request.POST)
        else:
            if self.object and self.object.message:
                context_data['message_form'] = MessageForm(instance=self.object.message)
            else:
                context_data['message_form'] = MessageForm()
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        message_form = context_data['message_form']
        self.object = form.save(commit=False)

        if message_form.is_valid() and self.request.user.is_authenticated:
            message = message_form.save()
            self.object.message = message
            self.object.owner = self.request.user
            self.object.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)


class OnlyForOwnerOrSuperuserMixin:
    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_superuser:
            raise Http404
        return self.object


class HomeView(MailingAndMessageSaveMixin, CreateView):
    model = Mailing
    template_name = 'mailing/home.html'
    form_class = MailingForm
    success_url = reverse_lazy('mailing:home')
    extra_context = {'button': 'Создать', }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            mailings = user.mailing_set.all()
            context['total_mailings'] = len(mailings)
            context['active_mailings'] = len(mailings.filter(status=Mailing.STATUSES[1][0]))
            context['unique_clients'] = len(user.client_set.values('email').distinct())
        context['object_list'] = BlogEntry.objects.order_by('?')[:3]
        return context


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    template_name = 'mailing/recipient_form.html'
    form_class = ClientForm
    success_url = reverse_lazy('mailing:recipients_list')
    extra_context = {
        'title': 'Создать контакт',
        'button': 'Создать',
    }

    def form_valid(self, form):
        last_name = self.request.POST.get('last_name', '').strip()
        first_name = self.request.POST.get('first_name', '').strip()
        father_name = self.request.POST.get('father_name', '').strip()

        full_name = f"{last_name} {first_name} {father_name}".strip().title()

        form.instance.name = full_name

        self.object = form.save()
        self.object.owner = self.request.user

        return super().form_valid(form)


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'mailing/recipients_list.html'

    def get_queryset(self):
        user = self.request.user
        is_manager = user.groups.filter(name='Managers').exists()
        if user.is_superuser or is_manager:
            queryset = super().get_queryset().all()
        else:
            queryset = super().get_queryset().filter(owner=user)
        return queryset.order_by('name')


class ClientUpdateView(LoginRequiredMixin, OnlyForOwnerOrSuperuserMixin, UpdateView):
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
        last_name = self.request.POST.get('last_name', '').strip()
        first_name = self.request.POST.get('first_name', '').strip()
        father_name = self.request.POST.get('father_name', '').strip()

        full_name = f"{last_name} {first_name} {father_name}".strip().title()

        form.instance.name = full_name

        return super().form_valid(form)


class ClientDeleteView(LoginRequiredMixin, OnlyForOwnerOrSuperuserMixin, DeleteView):
    model = Client
    template_name = 'mailing/recipient_delete.html'
    success_url = reverse_lazy('mailing:recipients_list')

    def get_context_data(self, **kwargs) -> dict:
        context_data = super().get_context_data(**kwargs)
        context_data['object'] = Client.objects.get(pk=self.kwargs.get('pk'))
        return context_data


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = 'mailing/mailing_list.html'

    def get_queryset(self):
        user = self.request.user
        is_manager = user.groups.filter(name='Managers').exists()
        if user.is_superuser or is_manager:
            queryset = super().get_queryset().all()
        else:
            queryset = super().get_queryset().filter(owner=user)
        return queryset.order_by('-updated_at')


class MailingCreateView(LoginRequiredMixin, MailingAndMessageSaveMixin, CreateView):
    model = Mailing
    template_name = 'mailing/mailing_form.html'
    form_class = MailingForm
    extra_context = {'button': 'Создать', 'title': 'Создать рассылку'}
    success_url = reverse_lazy('mailing:mailing_list')


class MailingUpdateView(LoginRequiredMixin, OnlyForOwnerOrSuperuserMixin, MailingAndMessageSaveMixin, UpdateView):
    model = Mailing
    template_name = 'mailing/mailing_form.html'
    form_class = MailingForm
    extra_context = {'button': 'Сохранить', 'title': 'Изменить рассылку'}
    success_url = reverse_lazy('mailing:mailing_list')


class MailingDeleteView(LoginRequiredMixin, OnlyForOwnerOrSuperuserMixin, DeleteView):
    model = Mailing
    template_name = 'mailing/mailing_delete.html'
    success_url = reverse_lazy('mailing:mailing_list')

    def get_context_data(self, **kwargs) -> dict:
        context_data = super().get_context_data(**kwargs)
        context_data['object'] = Mailing.objects.get(pk=self.kwargs.get('pk'))
        return context_data


class MailingDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Mailing
    template_name = 'mailing/mailing_card.html'

    def test_func(self):
        user = self.request.user
        is_manager = user.groups.filter(name='Managers').exists()
        is_owner = user == self.get_object().owner
        return user.is_superuser or is_manager or is_owner


def deactivate_mailing(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)
    mailing.status = Mailing.STATUSES[2][0]
    mailing.save()

    return redirect('mailing:mailing_list')

