# Generated by Django 5.0.1 on 2024-03-07 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_user_temporary_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='birthday',
            field=models.DateField(blank=True, null=True),
        ),
    ]
