
# path/to/your/proj/src/cfehome/celery.py
import os
from celery import Celery
from decouple import config
from celery.schedules import crontab
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rshome.settings')

app = Celery('rshome')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(['auctions'])


app.conf.beat_schedule = {
    'multiply-task-crontab': {
        'task': 'multiply_two_numbers',
        'schedule': crontab(hour=7, minute=30, day_of_week=1),
        'args': (16, 16),
    },
    'multiply-every-5-seconds': {
        'task': 'multiply_two_numbers',
        'schedule': 5.0,
        'args': (16, 16)
    },
    'add-every-30-seconds': {
        'task': 'movies.tasks.add',
        'schedule': 30.0,
        'args': (16, 16)
    },
}
