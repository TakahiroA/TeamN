from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser, models.Model):
    icon = models.ImageField(
        upload_to='img/',
        verbose_name='アイコン',
        blank=True,
    )


class Task(models.Model):
    PRIOLITY_NUMBER = (
        (0, '未選択'),
        (1, '最低'),
        (2, '低'),
        (3, '常'),
        (4, '高'),
        (5, '最高')
    )

    task_cd = models.AutoField(
        primary_key=True
    )

    task_name = models.CharField(
        max_length=100,
        verbose_name='タスク名'
    )

    user_name = models.CharField(
        max_length=30,
        null=True,
        blank=True,
        verbose_name='担当者名'
    )

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='担当者'
    )

    start_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='開始日'
    )

    end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='終了日'
    )

    details = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name='詳細'
    )

    priolity = models.IntegerField(
        choices=PRIOLITY_NUMBER,
        default=0
    )

    update_date = models.DateField(
        auto_now=True
    )

    is_delete = models.BooleanField(
        default=False
    )
