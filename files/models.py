import traceback
import uuid
from datetime import datetime, timedelta
from django.db import models
from user.models import User


class File(models.Model):
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4,
        editable=False
    )
    file_name = models.CharField(
        'nome do arquivo',
        max_length=100, 
        blank=True,
        null=True
    )
    folder_name = models.CharField(
        'nome da pasta destino',
        max_length=100,
        blank=True,
        null=True
    )
    uploaded_at = models.DateField(auto_now_add=True)
    expires_at = models.DateField(auto_now_add=True)
    period_to_expiration = models.CharField(
        'periodo (em dias) de expiração do arquivo',
        max_length=100, 
        blank=True,
        null=True
    )
    expire_notification = models.DateField(
        blank=True,
        null=True
    )
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT
    )

    class Meta:
        verbose_name = 'file'
        verbose_name_plural = 'files'
        db_table = 'tb_file'


    def register_file(files):
        uploaded_at = datetime.strptime(files.get("uploaded_at"), '%Y-%m-%d')
        expires_at=datetime.strptime(files.get("expires_at"), '%Y-%m-%d')
        period_to_expiration = int(files.get("period_to_expiration")) if files.get("period_to_expiration") else 30
        expire_notification = expires_at - timedelta(days=period_to_expiration)

        try:
            query = File.objects.create(
                file_name=files.get("file_name"),
                folder_name=files.get("folder_name"),
                uploaded_at=uploaded_at,
                expires_at=expires_at,
                user_id=files.get("user_id"),
                period_to_expiration=period_to_expiration,
                expire_notification=expire_notification
            )
            query.save()
            return query
        except Exception as error:
            print(error)
            traceback.print_exc()