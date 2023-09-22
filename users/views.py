import secrets

from django.contrib.auth.views import LoginView as BaseLoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from django.contrib import messages
from users import services
from users.forms import LoginForm, UserRegisterForm
from users.models import User


class LoginView(BaseLoginView):
    template_name = 'users/login.html'
    form_class = LoginForm


class RegisterView(CreateView):
    model = User
    template_name = 'users/registration.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save(commit=False)
            verification_code = secrets.token_urlsafe(nbytes=11)
            self.object.verification_code = verification_code

            url = reverse('users:verification', args=[verification_code])
            absolute_url = self.request.build_absolute_uri(url)
            services.send_verification_url(email=self.object.email,
                                           url=absolute_url)
            messages.success(self.request, 'Ссылка для верификации отправлена на вашу электронную почту!')
            self.object.save()

        return super().form_valid(form)


def verification(request, verification_code):

    user = User.objects.get(verification_code=verification_code)
    user.is_active = True
    user.verification_code = None
    user.save()
    return redirect(reverse('users:login'))

