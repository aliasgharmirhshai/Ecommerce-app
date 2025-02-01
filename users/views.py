from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from .forms import UserRegistrationForm

class UserRegisterView(CreateView):
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')
    template_name = 'users/register.html'

class UserLoginView(LoginView):
    template_name = 'users/login.html'

class UserLogoutView(LogoutView):
    next_page = 'login'
    http_method_names = ['get', 'post']

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        if response.status_code == 200:
            return redirect(self.next_page)
        return response













