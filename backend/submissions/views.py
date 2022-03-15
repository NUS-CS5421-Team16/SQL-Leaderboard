from django.shortcuts import render
from django.http import HttpResponse

from .models import Submission

# Create your views here.
def index(request):
    latest_leaderboard_list = Submission.objects.order_by('scores','times')
    output = '<br>'.join(["Team: " + s.team + ", Scores: "+ str(int(s.scores)) + ", Submission Times: " + str(int(s.times)) + "<br>" for s in latest_leaderboard_list])
    return HttpResponse(output)

def thanks(request, team_name):
    return HttpResponse("Thanks for your submission Team %s" % team_name)