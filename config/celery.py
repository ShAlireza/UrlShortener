from __future__ import absolute_import, unicode_literals
import os
from logging.config import dictConfig

from django.conf import settings
from celery import Celery
from celery.signals import setup_logging

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'config.settings')

app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')


@setup_logging.connect
def config_loggers(*args, **kwargs):
    dictConfig(settings.LOGGING)


app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
