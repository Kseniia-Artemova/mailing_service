from django.contrib import admin
from mailing.models import Client, Message, Log, Mailing

# Register your models here.


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'comment')
    search_fields = ('name', 'email')
    list_filter = ('name',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'body')
    search_fields = ('subject',)
    list_filter = ('subject',)


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('timedate', 'status', 'server_response')
    search_fields = ('timedate', 'status', 'server_response')
    list_filter = ('timedate', 'status', 'server_response')


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('timedate', 'frequency', 'status', 'message')
    search_fields = ('timedate', 'frequency', 'status', 'message')
    list_filter = ('timedate', 'frequency', 'status', 'message')
