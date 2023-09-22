from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from blog.forms import BlogEntryForm
from blog.models import BlogEntry


class BlogEntryListView(ListView):
    model = BlogEntry
    template_name = 'blog/blog_entry_list.html'


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
    pass


class BlogEntryDetailView(DetailView):
    pass