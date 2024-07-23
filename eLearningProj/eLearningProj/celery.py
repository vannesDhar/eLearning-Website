from __future__ import absolute_import

import os 
import time

from celery import Celery 
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eLearningProj.settings')

app = Celery('../eLearningProj')
app.config_from_object(settings, namespace='CELERY')
app.autodiscover_tasks()


