from django.conf import settings
from django.db import models

from competitor.models import Competitor, Competition


def get_task_path(instance, filename):
    return instance.get_task_path()


class Task(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending"
        RUNNING = "running"
        SUCCESS = "success"
        ERROR = "error"

    status = models.CharField(max_length=32, choices=Status.choices, blank=False, null=False, default=Status.PENDING)
    sql = models.FileField(upload_to=get_task_path, null=True)
    result = models.FloatField(null=True)
    start_time = models.DateTimeField(auto_now=True)
    end_time = models.DateTimeField(null=True)
    previous_task = models.ForeignKey('self', on_delete=models.CASCADE, null=True)

    def check_safety(self):
        pass

    def run(self, **kwargs):
        pass


class SetupTask(Task):
    class SetupTaskType(models.TextChoices):
        PRIVATE_CREATE = "private create"
        PUBLIC_CREATE = "public create"
        PRIVATE_QUERY = "private query"
        PUBLIC_QUERY = "public query"

    setup_type = models.CharField(max_length=32, choices=SetupTaskType.choices, blank=False, null=False)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, null=False)

    def get_task_path(self):
        return f"tasks/{self.__class__.__name__}/{self.setup_type}.sql"

    def run(self):
        if "create" in self.setup_type:
            save_result = False
        else:
            save_result = True

        if "private" in self.setup_type:
            database = settings.PRIVATE_DATABASE
        else:
            database = settings.PUBLIC_DATABASE

        super(SetupTask, self).run(save_result=save_result, database=database)


class QueryTask(Task):
    class QueryTaskType(models.TextChoices):
        PRIVATE = "private"
        PUBLIC = "public"

    query_type = models.CharField(max_length=32, choices=QueryTaskType.choices, null=True)
    competitor = models.ForeignKey(Competitor, on_delete=models.CASCADE, null=False)

    def get_task_path(self):
        return f"tasks/{self.__class__.__name__}/{self.competitor.name}.sql"

    def run(self):
        if "private" in self.setup_type:
            database = settings.PRIVATE_DATABASE
        else:
            database = settings.PUBLIC_DATABASE
        super(QueryTask, self).run(save_result=True, database=database)

        # update best_task of the team if needed
