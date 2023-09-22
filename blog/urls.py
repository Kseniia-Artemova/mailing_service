from django.urls import path
from blog.apps import BlogConfig
from blog.views import BlogEntryListView, BlogEntryCreateView, BlogEntryDeleteView, BlogEntryUpdateView

app_name = BlogConfig.name

urlpatterns = [
    path('', BlogEntryListView.as_view(), name='blog_entry_list'),
    path('create_entry/', BlogEntryCreateView.as_view(), name='create_entry'),
    path('delete_entry/<int:pk>/', BlogEntryDeleteView.as_view(), name='delete_entry'),
    path('update_entry/<int:pk>/', BlogEntryUpdateView.as_view(), name='update_entry'),
    path('entry_detail/<int:pk>/', BlogEntryUpdateView.as_view(), name='entry_detail'),
]
