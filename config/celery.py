from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

import ssl
ssl._create_default_https_context = ssl._create_unverified_context


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings") #
app = Celery("config") #создаем приложение celery
app.config_from_object("django.conf:settings", namespace="CELERY") #
app.autodiscover_tasks() # автоматически находит задачи