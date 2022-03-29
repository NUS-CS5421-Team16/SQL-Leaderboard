import os

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
app = Celery("sqltaskrunner")

app.conf.broker_url = 'redis://localhost:6379/0'

app.autodiscover_tasks()
