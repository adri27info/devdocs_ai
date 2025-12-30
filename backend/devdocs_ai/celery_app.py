from __future__ import absolute_import, unicode_literals

import os
from django.conf import settings
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "devdocs_ai.conf.settings")

app = Celery("devdocs_ai")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
