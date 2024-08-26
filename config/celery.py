import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'online_training.settings')

app = Celery('online_training')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
