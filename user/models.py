import uuid
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token
from .managers import CustomUserManager


class User(AbstractUser):
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4,
        editable=False
    )
    username = None
    email = models.EmailField('email address', unique=True)
    is_staff = models.BooleanField(
        null=True,
        blank=True,
        default=True
    )
    folder_name = models.CharField(
        max_length=150,
        null=True,
        blank=True
    )
    phone = models.CharField(
        max_length=150,
        null=True,
        blank=True
    )
    cpf_cnpj = models.CharField(
        max_length=150,
        null=True,
        blank=True
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        db_table = 'tb_user'

@receiver(post_save, sender=get_user_model())
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


