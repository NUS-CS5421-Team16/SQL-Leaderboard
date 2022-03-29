from celery.schedules import crontab
from django.db.transaction import atomic
from django.utils import timezone

from backend.celery import app as celery_app
from competition.models import Competition
from competitor.models import Team

from task.models import SetupTask, Task, QueryTask
from task.serializer import QueryTaskSerializer


@celery_app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=0, minute=0),
        update_remain_upload_times.s()
    )
    sender.add_periodic_task(5, find_and_run_task.s())
    sender.add_periodic_task(
        crontab(hour='*/2', minute=1), # check ddl every 2 hour
        check_competition_end_and_create_private_task.s()
    )


def try_run_task(task):
    with atomic():
        competition_instance = Competition.objects.first()
        concurrent_limit = competition_instance.concurrent_limit
        running_task_count = Task.objects.filter(status=Task.Status.RUNNING).count()
        if (task.previous_task is None or task.previous_task.status == Task.Status.SUCCESS \
                or task.previous_task.status == Task.Status.ERROR) and running_task_count < concurrent_limit:
            run = True
            task.status = Task.Status.RUNNING
            task.save()
        else:
            run = False
    if run:
        task.run()


# @celery_app.task
def check_competition_end_and_create_private_task():
    competition_instance = Competition.objects.first()
    if competition_instance.end_time > timezone.now():
        print("check_competition_end_and_create_private_task---competition is going on")
        return
    private_task = QueryTask.objects.filter(query_type=QueryTask.QueryTaskType.PRIVATE).first()
    if private_task is not None:
        print("check_competition_end_and_create_private_task---private query already created")
        return
    print("check_competition_end_and_create_private_task---create private query")
    for team in Team.objects.all():
        competitor_instance = team.competitor_set.first()
        if competitor_instance is None:
            continue
        latest_public_task = QueryTask.objects.filter(competitor__team=team).order_by("-start_time").first()

        if latest_public_task:
            serializer = QueryTaskSerializer(data={
                "sql": latest_public_task.sql,
                "query_type": QueryTask.QueryTaskType.PRIVATE,
                "competitor": competitor_instance.id
            })
            serializer.is_valid(raise_exception=True)
            serializer.save()


@celery_app.task
def update_remain_upload_times():
    competition_instance = Competition.objects.first()
    if competition_instance is None:
        return

    remain_upload_times = competition_instance.upload_limit
    for team in Team.objects.all():
        team.remain_upload_times = remain_upload_times
        team.save()
    print("update_remain_upload_times")


@celery_app.task
def find_and_run_task():
    # find task
    task = SetupTask.objects.filter(status=Task.Status.PENDING).order_by("id").first()
    if task is None:
        task = QueryTask.objects.filter(status=Task.Status.PENDING).order_by("id").first()
    if task is None:
        print("find_and_run_task---no task to run")
        return

    # try
    print("find_and_run_task---task(%s, %s): sql(%s)" % (task.id, task.__class__, task.sql))
    try_run_task(task)


@celery_app.task
def async_run_task(task_id, class_name):
    # get task
    print("async_run_task---task_id(%s) classname(%s)" % (task_id, class_name))
    if class_name == "setuptask":
        task = SetupTask.objects.get(pk=task_id)
    else:
        task = QueryTask.objects.get(pk=task_id)

    # try
    print("async_run_task---task(%s, %s): sql(%s)" % (task.id, task.__class__, task.sql))
    try_run_task(task)
