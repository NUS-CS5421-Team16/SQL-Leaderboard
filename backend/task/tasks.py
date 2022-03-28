from django.db import connections

from backend.celery import app as celery_app
from competition.models import Competition

from task.models import SetupTask, Task, QueryTask


@celery_app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(5, find_and_run_task.s())


def try_run_task(task):
    print("task(%s, %s): sql(%s)" % (task.id, task.__class__, task.sql))
    competition_instance = Competition.objects.first()
    concurrent_limit = competition_instance.concurrent_limit
    running_task_count = Task.objects.filter(status=Task.Status.RUNNING).count()
    if running_task_count < concurrent_limit:
        task.run()


@celery_app.task
def find_and_run_task():
    task = SetupTask.objects.filter(status=Task.Status.PENDING).order_by("id").first()
    if task is None:
        task = QueryTask.objects.filter(status=Task.Status.PENDING).order_by("id").first()
    if task is None:
        print("no task to run")
        return
    if task.previous_task is None or task.previous_task.status == Task.Status.SUCCESS \
            or task.previous_task.status == Task.Status.ERROR:
        try_run_task(task)


@celery_app.task
def async_run_task(task):
    try_run_task(task)
