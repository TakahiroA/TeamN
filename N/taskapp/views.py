from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView, LogoutView
)
from django.views import generic
from django.contrib.auth.decorators import login_required
from .forms import LoginForm
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model
from .forms import RegistrationForm

User = get_user_model()


"""ログインページ"""
class Login(LoginView):
    template_name = 'login.html'
    form_class = LoginForm


""" トップページ """
class Top(LoginRequiredMixin, generic.TemplateView):
    template_name = 'top.html'
    redirect_field_name = 'redirect_to'


"""ログアウトページ"""
class Logout(LoginRequiredMixin, LogoutView):
    template_name = 'logout.html'

    """アカウント登録ページ"""
class Registration(generic.CreateView):
    model = User
    template_name = 'registration.html'
    form_class = RegistrationForm
    success_url ='/registration/complete'


"""アカウント登録完了"""
class RegistrationComp(generic.TemplateView):
    template_name = 'registration_complete.html'