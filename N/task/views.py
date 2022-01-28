from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models.query import QuerySet
from django.views import generic
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect, render, resolve_url
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db import models
from .models import ProjectToUsers, Project
from .forms import ProjectCreate, Subject_all
from .forms import ProjectUpdate
from .forms import ProjectDelete
from .forms import AddProjectMember
from .forms import Follows
from .forms import Alreadys
from .forms import TaskUpdate
from django.http.response import JsonResponse
from django.core import serializers
from .models import ProjectToUsers, Project, ProjectToTask, Task,Subject,Follow,Already
from django.views.decorators.csrf import csrf_exempt 
import datetime
import cgi # CGIモジュールのインポート
import cgitb
import sys
from taskapp.models import Schedule
import logging
import sys



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
        now_data = datetime.date.today()
        near = datetime.date.today() + datetime.timedelta(days=4)
        context["near"] = near
        context["td_data"] = now_data



        if len(project_user) > 0:
            context['member'] = []
            for person in project_user:
                member = Project.objects.filter(project_cd=person.project_cd.pk, is_delete=0)
                context['member'].extend(member)
        else:
            context['member'] = None

        context['leader'] = leader if len(leader) > 0 else None

        return context

""" トップページ期限切れ """
class taskTop_out(LoginRequiredMixin, generic.TemplateView):
    template_name = 'task/task_top_out.html'
    redirect_field_name = 'redirect_to'

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)

        project_user = ProjectToUsers.objects.filter(user_cd=user.pk)
        leader = Project.objects.filter(leader=user.pk, is_delete=0)
        now_data = datetime.date.today()
        near = datetime.date.today() + datetime.timedelta(days=4)
        context["near"] = near
        context["td_data"] = now_data



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

    def form_valid(self, form):
        end_date = form.cleaned_data.get('end_date')
        name = form.cleaned_data.get('name')           
        obj= Schedule(date= end_date, summary= name)
        obj.save()
        return super().form_valid(form)

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
class ProjectPage(LoginRequiredMixin, generic.TemplateView):
    model = Subject,Follow
    template_name = 'task/our_project.html'
    form_class = Subject_all
    success_url ='task/follow.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        
        subject = Subject.objects.all()
        
        context['subject'] = subject
        
        return context

    def post(self, request, *args, **kwargs):
        check = request.POST.getlist('subjects')
        for sub in check:
            query = Subject.objects.filter(subject_cd=sub)  
            obj = Follow(subject_cd=query[0].subject_cd,subject_name=query[0].subject_name)
            obj.save()
        return redirect("/")

""" フォロー科目ページ """
class FollowPage(LoginRequiredMixin, generic.TemplateView):
    model = Follow
    template_name = 'task/follow.html'
    form_class = Follows
    

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        
        follow = Follow.objects.all()
        
        context['follow'] = follow
        
        return context

""" 提出済み課題ページ """
class AlreadyPage(LoginRequiredMixin, generic.TemplateView):
    
    template_name = 'task/already.html'
    form_class = Alreadys
    

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)

        project_user = ProjectToUsers.objects.filter(user_cd=user.pk)
        leader = Project.objects.filter(leader=user.pk, is_delete=0)
        now_data = datetime.date.today()
        context["td_data"] = now_data



        if len(project_user) > 0:
            context['member'] = []
            for person in project_user:
                member = Project.objects.filter(project_cd=person.project_cd.pk, is_delete=0)
                context['member'].extend(member)
        else:
            context['member'] = None

        context['leader'] = leader if len(leader) > 0 else None

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

""" 提出済み更新ページ """
class TaskUpdate(ProjectUserOnlyMixin, generic.UpdateView):
    model = Project
    template_name = 'task/task_update.html'
    form_class = TaskUpdate

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

        return {'is_already': True,}

    def get_success_url(self):
        project = Project.objects.filter(project_cd=self.kwargs["pk"], is_delete=0)
        Schedule.objects.filter(summary=project[0].name).delete()
        return resolve_url('task:task_top')


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
        Schedule.objects.filter(summary=project[0].name).delete()
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
        return resolve_url('task:already')

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
    

""" タスク追加 """
class AddTaskForAjax():

    def ajax_response(self, *args, **kwargs):
        taskName = 'sample'

        if self.POST.get('user') != "":
            user = self.POST.get('user')
        else:
            user = None

        if user == None:
            userName = self.POST.get('userName') if self.POST.get('userName') != "" else None
        else:
            userName = None

        details = self.POST.get('details') if self.POST.get('details') != "" else None
        startDate = self.POST.get('startDate') if self.POST.get('startDate') != "" else None
        endDate = self.POST.get('endDate') if self.POST.get('endDate') != "" else None
        priolity = '1'

        task = Task.objects.create(
            task_name=taskName, user=user,
            user_name=userName, details=details,
            start_date=startDate, end_date=endDate,
            priolity=priolity
        )

        projectCd = Project.objects.filter(project_cd=self.kwargs['pk'])
        project = Project.objects.get(project_cd=projectCd)

        result = ProjectToTask.objects.create(
            project_cd=project, task_cd=task
        )   

        projectTask = ManupilateDataBase.getProjectTask(projectCd)
        json_serializer = serializers.get_serializer("json")()
        taskData = json_serializer.serialize(projectTask, ensure_ascii=False)

        return JsonResponse({"taskdata" : taskData})
        


""" DB操作クラス """
class ManupilateDataBase():

    def getJoinProject(joinCd):
        p_user = ProjectToUsers.objects.filter(user_cd=joinCd)

        if len(p_user) > 0:
            result = []
            for p in p_user:
                member = Project.objects.filter(project_cd=p.project_cd.pk, is_delete=0)
                result.extend(member)
        else:
            result = None

        return result

    def getProjectTask(projectCd):
        p_task = ProjectToTask.objects.filter(project_cd=projectCd)

        if len(p_task) > 0:
            result = []
            for t in p_task:
                task = Task.objects.filter(pk=t.task_cd.pk)
                result.extend(task)
        else:
            result = None

        return result

    def getProjectMenber(memberCd):
        p_user = ProjectToUsers.objects.filter(project_cd=memberCd)

        if len(p_user) > 0:
            result = []
            for person in p_user:
                member = User.objects.filter(pk=person.user_cd.pk)
                result.extend(member)
        else:
            result = None

        return result

    def getTaskInfo(taskCd):
        task = Task.objects.filter(task_cd=taskCd)

        if len(task) > 0:
            return task
        else:
            return None

    def getUserInfo(userCd):
        user = User.objects.filter(use_cd=userCd)

        if len(user) > 0:
            return user
        else:
            return None

""" プロジェクトタスク情報取得 """
class getProjectTaskInfoAjax():

    @csrf_exempt 
    def ajax_response(self, *args, **kwargs):
        task_cd = self.POST['task_cd']

        projectTask = ManupilateDataBase.getTaskInfo(task_cd)

        if (projectTask[0].user != None):
            projectTask[0].user_name = projectTask[0].user.username

        json_serializer = serializers.get_serializer("json")()
        taskData = json_serializer.serialize(projectTask, ensure_ascii=False)

        return JsonResponse({"taskdata" : taskData})