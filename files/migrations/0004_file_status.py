# Generated by Django 5.0.1 on 2024-01-15 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0003_alter_file_expires_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='status',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Status do arquivo'),
        ),
    ]
