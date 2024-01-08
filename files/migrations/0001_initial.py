# Generated by Django 5.0.1 on 2024-01-08 15:15

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('file_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='nome do arquivo')),
                ('folder_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='nome da pasta destino')),
                ('uploaded_at', models.DateField(auto_now_add=True)),
                ('expires_at', models.DateField(auto_now_add=True)),
                ('period_to_expiration', models.CharField(blank=True, max_length=100, null=True, verbose_name='periodo (em dias) de expiração do arquivo')),
            ],
            options={
                'verbose_name': 'file',
                'verbose_name_plural': 'files',
                'db_table': 'tb_file',
            },
        ),
    ]
