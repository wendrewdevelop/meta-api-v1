# Generated by Django 5.0.1 on 2024-01-08 22:34

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('files', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('file_expiration_date', models.CharField(max_length=100, verbose_name='data de expiração do arquivo')),
                ('today_date', models.CharField(max_length=100, verbose_name='data atual')),
                ('status_notification', models.CharField(max_length=260, verbose_name='status da notificação')),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='files.file')),
            ],
            options={
                'verbose_name': 'notification',
                'verbose_name_plural': 'notifications',
                'db_table': 'tb_notification',
            },
        ),
    ]
