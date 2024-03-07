import traceback
import uuid
from datetime import datetime, timedelta
from django.db import models
from user.models import User


class Folder(models.Model):
    """
        folder_type = (subfolder, folder)
    """
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4,
        editable=False
    )
    user_root_folder = models.CharField(
        'nome da pasta raiz',
        max_length=100, 
        blank=True,
        null=True
    )
    folder_name = models.CharField(
        'nome da pasta',
        max_length=100, 
        blank=True,
        null=True
    )
    folder_type = models.CharField(
        'tipo da pasta',
        max_length=100, 
        blank=True,
        null=True
    )
    created_at = models.DateField(auto_now_add=True)
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT
    )

    class Meta:
        verbose_name = 'folder'
        verbose_name_plural = 'folders'
        db_table = 'tb_folder'


    def register_folder(folders):
        try:
            query = Folder.objects.create(
                folder_name=folders.get("folder_name"),
                folder_type=folders.get("folder_type", None),
                user_id=folders.get("user_id"),
                user_root_folder=folders.get("user_root_folder")
            )
            query.save()
            return query
        except Exception as error:
            print(error)
            traceback.print_exc()