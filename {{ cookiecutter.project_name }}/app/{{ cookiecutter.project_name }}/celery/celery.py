from __future__ import absolute_import
import os
from celery import Celery
from django.apps import AppConfig
from django.conf import settings


if not settings.configured:
    # set the default Django settings module for the 'celery' program.
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{{ cookiecutter.project_name }}.settings")  # pragma: no cover

app = Celery(
    "{{ cookiecutter.project_name }}",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS, force=True)
