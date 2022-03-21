from django.contrib.auth.models import User
from django.db import models

from competition.models import Competition


class Team(models.Model):
    uuid = models.CharField(max_length=256, blank=False, null=False)
    name = models.CharField(max_length=128)
    remain_upload_times = models.IntegerField(blank=False, null=False)
    best_private_task = models.ForeignKey("task.QueryTask", on_delete=models.CASCADE, null=True, related_name='private_team', related_query_name='private_team')
    best_public_task = models.ForeignKey("task.QueryTask", on_delete=models.CASCADE, null=True, related_name='public_team', related_query_name='public_team')


class Competitor(User):
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
