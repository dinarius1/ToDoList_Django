from django.contrib import admin
from .models import Task,TaskRequest

# Register your models here.
admin.site.register(Task)
admin.site.register(TaskRequest)