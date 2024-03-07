# Generated by Django 5.0.1 on 2024-03-07 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('folders', '0003_folder_user_root_folder'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='folder',
            name='subfolder_name',
        ),
        migrations.AddField(
            model_name='folder',
            name='folder_type',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='tipo da pasta'),
        ),
    ]