# Generated by Django 5.0.1 on 2024-03-07 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('folders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='folder',
            name='subfolder_name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='nome da subpasta'),
        ),
    ]
