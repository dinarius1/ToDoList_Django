# Generated by Django 5.0.7 on 2024-08-05 14:15

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0003_alter_task_contributors'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='contributors',
            field=models.ManyToManyField(blank=True, related_name='tasks', to=settings.AUTH_USER_MODEL),
        ),
    ]
