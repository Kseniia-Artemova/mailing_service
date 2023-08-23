from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import HomeView, ClientCreateView

app_name = MailingConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('new_recipient/', ClientCreateView.as_view(), name='new_recipient'),
]
