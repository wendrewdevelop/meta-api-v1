from django.db import models
from user.models import User
from files.models import File


class Notification(models.Model):
    file_expiration_date = models.CharField(
        'data de expiração do arquivo',
        max_length=100
    )
    today_date = models.CharField(
        'data atual',
        max_length=100
    )
    status_notification = models.CharField(
        'status da notificação',
        max_length=260
    )
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT
    )
    file = models.ForeignKey(
        File,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'notification'
        verbose_name_plural = 'notifications'
        db_table = 'tb_notification'
