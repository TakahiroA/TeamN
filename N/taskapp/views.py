from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.views import generic
from django.contrib.auth.decorators import login_required
from .forms import LoginForm
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model
from .forms import RegistrationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, resolve_url
from .forms import LoginForm, RegistrationForm, AccountsUpdateForm
from task.models import ProjectToUsers, Project
from django.views import generic
from . import mixins
from .models import Schedule


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

""" ユーザ限定クラス """
class UserOnlyMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return user.pk == self.kwargs['pk'] or user.is_superuser


""" ユーザ情報表示ページ """
class Profile(UserOnlyMixin, generic.DetailView):
    model = User
    template_name = 'profile.html'


""" ユーザ情報更新ページ """
class ProfileUpdate(UserOnlyMixin, generic.UpdateView):
    model = User
    form_class = AccountsUpdateForm
    template_name = 'profile_update.html'

    def get_success_url(self):
        return resolve_url('taskapp:profile', pk=self.kwargs['pk'])

""" パスワード変更ページ """
class PasswordChange(UserOnlyMixin, PasswordChangeView):
    model = User
    template_name = 'password_change.html'

    def get_success_url(self):
        return resolve_url('taskapp:password_complete', pk=self.kwargs['pk'])

""" パスワード変更完了 """
class PasswordChangeComplete(UserOnlyMixin, PasswordChangeDoneView):
    template_name = 'password_change_complete.html'

class MonthWithScheduleCalendar(mixins.MonthWithScheduleMixin, generic.TemplateView):
    """スケジュール付きの月間カレンダーを表示するビュー"""
    model = Schedule
    template_name = 'top.html'
    date_field = 'date'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)
        return context