from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import HomeView, ClientCreateView, ClientListView, ClientUpdateView, ClientDeleteView
from mailing.views import MailingListView, MailingCreateView, MailingUpdateView, MailingDeleteView

app_name = MailingConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('new_recipient/', ClientCreateView.as_view(), name='new_recipient'),
    path('recipients_list/', ClientListView.as_view(), name='recipients_list'),
    path('<int:pk>/update_recipient/', ClientUpdateView.as_view(), name='update_recipient'),
    path('<int:pk>/delete_recipient/', ClientDeleteView.as_view(), name='delete_recipient'),
    path('mailing_list/', MailingListView.as_view(), name='mailing_list'),
    path('new_mailing/', MailingCreateView.as_view(), name='new_mailing'),
    path('<int:pk>/update_mailing/', MailingUpdateView.as_view(), name='update_mailing'),
    path('<int:pk>/delete_mailing/', MailingDeleteView.as_view(), name='delete_mailing'),
]
