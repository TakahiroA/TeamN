# Generated by Django 3.2.9 on 2021-12-08 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0003_project_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='kamoku',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='科目名'),
        ),
    ]
