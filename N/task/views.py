from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import generic
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect, resolve_url
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db import models
from .models import ProjectToUsers, Project
from .forms import ProjectCreate
from .forms import ProjectUpdate
from .forms import ProjectDelete
from .forms import AddProjectMember


User = get_user_model()


""" トップページ """
class taskTop(LoginRequiredMixin, generic.TemplateView):
    template_name = 'task/task_top.html'
    redirect_field_name = 'redirect_to'

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)

        project_user = ProjectToUsers.objects.filter(user_cd=user.pk)
        leader = Project.objects.filter(leader=user.pk, is_delete=0)

        if len(project_user) > 0:
            context['member'] = []
            for person in project_user:
                member = Project.objects.filter(project_cd=person.project_cd.pk, is_delete=0)
                context['member'].extend(member)
        else:
            context['member'] = None

        context['leader'] = leader if len(leader) > 0 else None

        return context

""" プロジェクト作成 """
class BuildProject(LoginRequiredMixin, generic.CreateView):
    model = Project
    form_class = ProjectCreate
    success_url ='/task/'
    template_name = 'task/build_project.html'

    def get_initial(self): 
        leader = self.request.user.pk
        return {'leader': leader,}

""" プロジェクト限定 """
class ProjectUserOnlyMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        is_return = True

        user = self.request.user

        l_result = Project.objects.filter(leader=user.pk, project_cd=self.kwargs["pk"])
        m_result = ProjectToUsers.objects.filter(project_cd=self.kwargs["pk"], user_cd=self.request.user.pk)
        p_result = Project.objects.filter(project_cd=self.kwargs["pk"], is_delete=0)
        if len(l_result) == 0 and len(m_result) == 0:
            is_return = False

        if len(p_result) == 0:
            is_return = False

        return is_return

""" プロジェクトページ """
class ProjectPage(ProjectUserOnlyMixin, generic.TemplateView):
    template_name = 'task/our_project.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        
        project = Project.objects.filter(project_cd=self.kwargs["pk"])
        p_user = ProjectToUsers.objects.filter(project_cd=self.kwargs["pk"])

        if len(p_user) > 0:
            context['member'] = []
            for person in p_user:
                member = User.objects.filter(pk=person.user_cd.pk)
                context['member'].extend(member)
        else:
            context['member'] = None

        context['project'] = project if len(project) > 0 else None
        context['task'] = None

        return context

""" プロジェクトリーダ限定 """
class ProjectLeaderOnlyMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        is_return = True

        user = self.request.user

        l_result = Project.objects.filter(leader=user.pk, project_cd=self.kwargs["pk"])
        p_result = Project.objects.filter(project_cd=self.kwargs["pk"], is_delete=0)

        if len(l_result) == 0:
            is_return = False

        if len(p_result) == 0:
            is_return = False

        return is_return


""" プロジェクト情報 """
class ProjectDetail(ProjectUserOnlyMixin, generic.DetailView):
    model = Project
    template_name = 'task/project_detail.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)

        p_user = ProjectToUsers.objects.filter(project_cd=self.kwargs["pk"])
        project = Project.objects.filter(project_cd=self.kwargs["pk"], is_delete=0)

        context['member'] = p_user if len(p_user) > 0 else None

        context['project'] = project if len(project) > 0 else None

        return context


""" プロジェクト更新ページ """
class ProjectUpdate(ProjectUserOnlyMixin, generic.UpdateView):
    model = Project
    template_name = 'task/project_update.html'
    form_class = ProjectUpdate


    def get_success_url(self):
        return resolve_url('task:our_project_detail', pk=self.kwargs["pk"])


""" プロジェクト削除ページ """
class ProjectDelete(ProjectLeaderOnlyMixin, generic.UpdateView):
    model = Project
    template_name = 'task/project_delete.html'
    form_class = ProjectDelete

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)

        p_user = ProjectToUsers.objects.filter(project_cd=self.kwargs["pk"])
        project = Project.objects.filter(project_cd=self.kwargs["pk"], is_delete=0)

        if len(p_user) > 0:
            context['member'] = []
            for person in p_user:
                member = User.objects.filter(pk=person.user_cd.pk)
                context['member'].extend(member)
        else:
            context['member'] = None

        context['project'] = project if len(project) > 0 else None

        return context

    def get_initial(self): 
        return {'is_delete': True,}

    def get_success_url(self):
        return resolve_url('task:task_top')

""" プロジェクトメンバー追加 """

""" プロジェクトメンバー更新 """
class UpdateProjectMember(ProjectUserOnlyMixin, generic.CreateView):
    model = ProjectToUsers
    template_name = "task/update_member.html"
    form_class = AddProjectMember

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)

        p_user = ProjectToUsers.objects.filter(project_cd=self.kwargs["pk"])
        project = Project.objects.filter(project_cd=self.kwargs["pk"], is_delete=0)

        context['member'] = p_user if len(p_user) > 0 else None

        context['project'] = project if len(project) > 0 else None

        return context

    def get_success_url(self):
        return resolve_url('task:update_member', pk=self.kwargs["pk"])

    def get_initial(self): 
        pc = self.kwargs["pk"]
        return {'project_cd': pc,}


""" プロジェクトメンバー削除 """
class ProjectDeleteMember(ProjectLeaderOnlyMixin, generic.DeleteView):
    model = ProjectToUsers

    def delete(self, *args, **kwargs):
        delete=1
        delete_ids = self.request.POST.getlist('delete_ids')
        if delete_ids:
            ProjectToUsers.objects.filter(id__in=delete_ids).delete()

        return redirect('task:update_member', pk=self.kwargs["pk"])