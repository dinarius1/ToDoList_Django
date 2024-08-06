# from django.db.models.signals import post_save
# from django.dispatch import receiver
# # from task.models import TaskRequest
#
# @receiver(post_save, sender=TaskRequest)
# def auto_delete_task_request(sender, instance, **kwargs):
#     if not instance.is_active:
#         instance.delete()
