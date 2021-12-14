from django import forms
from .models import Project, ProjectToUsers, Subject
from taskapp.forms import User

""" プロジェクト作成 """
class ProjectCreate(forms.ModelForm):

    class Meta:
        model = Project
        fields = (
            'name', 'leader',
            'start_date', 'end_date',
            'details','url',
        )
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        self.fields['leader'].widget.attrs['hidden'] = 'true'
        self.fields['start_date'].widget.input_type = "date"
        self.fields['end_date'].widget.input_type="date"
        self.fields['url'].widget.input_type="string"

""" 課題提出Check """
class Kadaicheckf(forms.ModelForm):

    class Meta:
        model = Project
        fields = (
            'check',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['check'].queryset = '提出済み'

""" プロジェクト更新 """
class ProjectUpdate(forms.ModelForm):

    class Meta:
        model = Project
        fields = (
            'name',
            'start_date', 'end_date',
            'details','url',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        self.fields['start_date'].widget.input_type = "date"
        self.fields['end_date'].widget.input_type="date"
        self.fields['url'].widget.input_type="string"

class Subject_all(forms.ModelForm):
    class Meta:
        model = Subject
        fields = (
            'subject_name',
        )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subject_name'].widget.input_type="string"
     

""" プロジェクト削除 """
class ProjectDelete(forms.ModelForm):

    class Meta:
        model = Project
        fields = (
            'is_delete',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['is_delete'].widget.attrs['hidden'] = 'true'

""" メンバー追加 """
class AddProjectMember(forms.ModelForm):

    class Meta:
        model = ProjectToUsers
        fields = (
            'project_cd',
            'user_cd'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        where = []

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        self.fields['project_cd'].widget.attrs['hidden'] = 'true'

        leader = Project.objects.filter(project_cd=self.initial["project_cd"])
        in_member = ProjectToUsers.objects.filter(project_cd=self.initial["project_cd"])
        staff = User.objects.filter(is_staff=1)
        non_active = User.objects.filter(is_active=0)

        where.append(leader[0].leader_id)
        for in_men in in_member:
            where.append(in_men.user_cd_id) 

        for s in staff:
            where.append(s.pk)

        for non in non_active:
            where.append(non.pk)
            user = self.request.user

        result = User.objects.exclude()

        self.fields['user_cd'].queryset = result

