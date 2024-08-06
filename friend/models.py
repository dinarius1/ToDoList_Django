from django.db import models
from django.conf import settings
from task.models import Task

class FriendUser(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_friend')
    friend = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='friend_user')
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='friend_task')
    right_to_read = models.BooleanField(default=False)
    right_to_update = models.BooleanField(default=False)
    def __str__(self):
        return str(self.friend)

class FriendList(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_list')
    friends = models.ManyToManyField(FriendUser, related_name='friend_list', blank=True)

    def __str__(self):
        return str(self.user)

class FriendRequest(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_requests')
    receiver = models.EmailField(max_length=100, blank=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='request_task')
    right_to_read = models.BooleanField(default=False)
    right_to_update = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


