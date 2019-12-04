from celery import shared_task


@shared_task(take_limit=60 * 5)
def example_celerybeat_task():
    print("Hello {{ cookiecutter.project_name }}!")
