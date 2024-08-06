from django.db import models
from django.conf import settings


class Task(models.Model):
    # Связь с пользователем, который создал задачу
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_tasks')
    # Связь с пользователем, которому назначены права
    contributors = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='tasks', blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    priority = models.IntegerField(choices=[(1,1),(2,2), (3,3)])
    deadline = models.DateTimeField(auto_now=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class TaskRequest(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='sent_requests')
    receiver = models.EmailField(max_length=100, blank=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='request_task')
    is_active = models.BooleanField(default=True)


    def save(self, *args, **kwargs):
        # First, save the instance to ensure it has a primary key
        super().save(*args, **kwargs)


# class Contributors(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_list')
#     contributor = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='contributors', blank=True)