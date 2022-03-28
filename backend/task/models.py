from django.conf import settings
from django.db import models, connections
from django.db.utils import DatabaseError

from competitor.models import Competitor, Competition

CAL_TIME_SQL = """
CREATE OR REPLACE FUNCTION caltime (TEXT) RETURNS TEXT AS
$$
DECLARE
r RECORD;
p TEXT;
e TEXT;
ap NUMERIC := 0;
ae NUMERIC := 0;
total NUMERIC := 0;
BEGIN
FOR r in EXECUTE 'EXPLAIN ANALYZE ' || $1
LOOP
	IF  r::TEXT LIKE '%Planning%'
	THEN 
	p := regexp_replace( r::TEXT, '.*Planning (?:T|t)ime: (.*) ms.*', '\1');
	END IF;
	IF r::TEXT LIKE '%Execution%'
	THEN 
	e := regexp_replace( r::TEXT, '.*Execution (?:T|t)ime: (.*) ms.*', '\1');
	END IF;
END LOOP;
ap := ap + (p::NUMERIC - ap);
ae := ae + (e::NUMERIC - ae);
total = ap + ae;
RETURN ROUND(total, 2);
END;
$$ LANGUAGE plpgsql;
"""


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
        sql = ""
        if "create" in self.setup_type:
            save_result = False
            sql += CAL_TIME_SQL
        else:
            save_result = True

        if "private" in self.setup_type:
            database = settings.PRIVATE_DATABASE
        else:
            database = settings.PUBLIC_DATABASE

        self.status = Task.Status.RUNNING
        self.save()

        with self.sql.open('r') as file:
            sql += file.read()

        try:
            with connections[database].cursor() as cursor:
                cursor.execute(sql)
                if save_result:
                    rows = cursor.fetchall()
                    setattr(self.competition, f"{database}_result", str(rows))
                    self.competition.save()

            self.status = Task.Status.SUCCESS
            self.save()
        except DatabaseError as e:
            setattr(self.competition, f"{database}_result", str(e))
            self.competition.save()
            self.status = Task.Status.ERROR
            self.save()
            print(e)


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
