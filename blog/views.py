from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from blog.forms import BlogEntryForm
from blog.models import BlogEntry


class BlogEntryListView(ListView):
    model = BlogEntry
    template_name = 'blog/blog_entry_list.html'
    ordering = '-publication_date'


class BlogEntryCreateView(CreateView):
    model = BlogEntry
    form_class = BlogEntryForm
    template_name = 'blog/blog_entry_form.html'
    success_url = reverse_lazy('blog:blog_entry_list')
    extra_context = {
        'title': 'Создать запись блога',
        'button': 'Создать',
    }


class BlogEntryUpdateView(UpdateView):
    model = BlogEntry
    form_class = BlogEntryForm
    template_name = 'blog/blog_entry_form.html'
    success_url = reverse_lazy('blog:blog_entry_list')
    extra_context = {
        'title': 'Изменить запись блога',
        'button': 'Сохранить',
    }


class BlogEntryDeleteView(DeleteView):
    model = BlogEntry
    template_name = 'blog/blog_entry_delete.html'
    success_url = reverse_lazy('blog:blog_entry_list')


class BlogEntryDetailView(DetailView):
    model = BlogEntry
    template_name = 'blog/blog_entry_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['referer'] = self.request.META.get('HTTP_REFERER')
        return context

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        self.object.views_number += 1
        self.object.save()

        return response
