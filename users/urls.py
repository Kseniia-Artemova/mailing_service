from django.contrib.auth.views import LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import RegisterView, LoginView, verification, UserUpdateView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registration/', RegisterView.as_view(), name='registration'),
    path('verification/<str:verification_code>/', verification, name='verification'),
    path('profile/', UserUpdateView.as_view(), name='profile'),
]