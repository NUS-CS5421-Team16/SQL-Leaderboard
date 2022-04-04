from django.conf import settings
from django.db import models, connections
from django.db.utils import DatabaseError
from django.utils import timezone

from competitor.models import Competitor, Competition


# create a function to calculate planning and execution time
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
	p := regexp_replace( r::TEXT, '.*Planning (?:T|t)ime: (.*) ms.*', '\\1');
	END IF;
	IF r::TEXT LIKE '%Execution%'
	THEN 
	e := regexp_replace( r::TEXT, '.*Execution (?:T|t)ime: (.*) ms.*', '\\1');
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
            self.end_time = timezone.now()
            self.save()
        except DatabaseError as e:
            setattr(self.competition, f"{database}_result", str(e))
            self.competition.save()
            self.status = Task.Status.ERROR
            self.end_time = timezone.now()
            self.save()
            print(e)


class QueryTask(Task):
    class QueryTaskType(models.TextChoices):
        PRIVATE = "private"
        PUBLIC = "public"

    dangerous_ops = ['update', 'create', 'delete', 'alter', 'drop', 'truncate', 'insert']

    query_type = models.CharField(max_length=32, choices=QueryTaskType.choices, null=True)
    competitor = models.ForeignKey(Competitor, on_delete=models.CASCADE, null=False)
    error_message = models.TextField(null=True)

    def get_task_path(self):
        return f"tasks/{self.__class__.__name__}/{self.competitor.username}.sql"

    def run(self):
        if "private" in self.query_type:
            database = settings.PRIVATE_DATABASE
        else:
            database = settings.PUBLIC_DATABASE

        running_time_limit = self.competitor.competition.running_time_limit
        reference_result = getattr(self.competitor.competition, "%s_result" % database)
        team = self.competitor.team
        best_task = getattr(team, "best_%s_task" % database)

        with self.sql.open('r') as file:
            sql = file.read()
        try:
            # run sql 2 times
            # check the result
            with connections[database].cursor() as cursor:
                cursor.execute("set statement_timeout={0}".format(running_time_limit * 1000))
                cursor.execute(sql)
                rows = cursor.fetchall()

            if str(rows) == reference_result:
                # if same result, track time
                with connections[database].cursor() as cursor:
                    sql = "SELECT caltime('" + sql + "');"
                    cursor.execute("set statement_timeout={0}".format(running_time_limit * 1000))
                    cursor.execute(sql)
                    row = cursor.fetchone()
                    print(f"query time:{row[0]}ms")
                    self.status = Task.Status.SUCCESS
                    self.result = float(row[0])
                    self.end_time = timezone.now()
                    self.save()

                # update best_task of the team if needed
                if best_task is None or best_task.result > self.result:
                    print("set best")
                    setattr(team, 'best_%s_task' % database, self)
                    team.save()
            else:
                # if different result, error
                self.status = Task.Status.ERROR
                self.error_message = "different result from reference sql"
                self.end_time = timezone.now()
                self.save()
        except DatabaseError as e:
            self.status = Task.Status.ERROR
            self.error_message = f"DatabaseError: {str(e)}"
            self.end_time = timezone.now()
            self.save()
            print(e)
