from django.contrib.auth import login, authenticate, get_user_model, logout
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.backends import ModelBackend
from .forms import UserRegistrationForm

User = get_user_model()

class UserRegisterView(CreateView):
    template_name = 'users/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        response = super().form_valid(form)
        email = form.cleaned_data.get('email')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(self.request, email=email, password=raw_password)
        if user:
            login(self.request, user)
        return response

class CustomAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            try:
                user = User.objects.get(phone_number=username)
            except User.DoesNotExist:
                return None
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None

class UserLoginView(LoginView):
    template_name = 'users/login.html'


class UserLogoutView(LogoutView):
    next_page = 'login'  # Ensure 'login' is the correct URL name

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return redirect(self.next_page)


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'users/dashboard.html'
