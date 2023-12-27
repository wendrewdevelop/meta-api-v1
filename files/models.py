import traceback
from django.db import models
from user.models import User


class File(models.Model):
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
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT
    )

    class Meta:
        verbose_name = 'file'
        verbose_name_plural = 'files'
        db_table = 'tb_file'


    def register_file(files):
        query = File.objects.create(
            file_name=files.get("file_name"),
            folder_name=files.get("folder_name"),
            uploaded_at=files.get("uploaded_at"),
            expires_at=files.get("expires_at"),
            user_id=files.get("user_id"),
            period_to_expiration=files.get("period_to_expiration") if files.get("period_to_expiration") else 30
        )
        try:
            query.save()
            return query
        except Exception as error:
            print(error)
            traceback.print_exc()