
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('task', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='担当者'),
        ),
        migrations.AddField(
            model_name='projecttousers',
            name='project_cd',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='task.project'),
        ),
        migrations.AddField(
            model_name='projecttousers',
            name='user_cd',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='projecttotask',
            name='project_cd',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='task.project'),
        ),
        migrations.AddField(
            model_name='projecttotask',
            name='task_cd',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='task.task'),
        ),
        migrations.AddField(
            model_name='project',
            name='leader',
<<<<<<< HEAD
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leader', to=settings.AUTH_USER_MODEL, verbose_name='講師'),
=======
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leader', to=settings.AUTH_USER_MODEL, verbose_name='科目名'),
>>>>>>> 100f4291c465dbdc37a5000943b55b8fa7d9ee3b
        ),
    ]
