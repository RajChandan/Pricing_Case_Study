from __future__ import absolute_import, unicode_literals
import os
import multiprocessing
from celery import Celery

if os.name == 'nt':  # 'nt' indicates Windows
    multiprocessing.set_start_method('spawn', force=True)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pricing_case_study.settings')

app = Celery('pricing_case_study')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
