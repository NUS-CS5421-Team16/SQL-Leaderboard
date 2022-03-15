from django.db import models

# Create your models here.
class Submission(models.Model):
    team = models.CharField(max_length=100,primary_key=True)
    scores = models.FloatField(null=True)
    # ranking = models.IntegerField()
    times = models.IntegerField()
    time_stamp = models.DateTimeField(auto_now_add=True) #created_at

    def __str__(self):
        #return the team name
        return self.team
