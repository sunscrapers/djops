import logging
import shlex
import subprocess

from django.core.management.base import BaseCommand
from django.utils import autoreload


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def restart_celery_beat():
    subprocess.call(shlex.split("pkill celery"))
    subprocess.call(
        shlex.split(
            "celery "
            "-A {{ cookiecutter.project_name }}.celery "
            "-S django beat "
            "-l debug"
        )
    )


class Command(BaseCommand):

    def handle(self, *args, **options):
        logger.info("Starting development celery beat with autoreload...")
        autoreload.run_with_reloader(restart_celery_beat)
