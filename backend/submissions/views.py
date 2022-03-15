from django.shortcuts import render
from django.http import HttpResponse

# parsing data from the client
from rest_framework.parsers import JSONParser

# To bypass having a CSRF token
from django.views.decorators.csrf import csrf_exempt

# for sending response to the client
from django.http import HttpResponse, JsonResponse

# API definition for task
from .serializers import SubmissionSerializer

# Task model
from .models import Submission

# Create your views here.
def index(request):
    latest_leaderboard_list = Submission.objects.order_by('scores','times')
    output = '<br>'.join(["Team: " + s.team + ", Scores: "+ str(int(s.scores)) + ", Submission Times: " + str(int(s.times)) + "<br>" for s in latest_leaderboard_list])
    return HttpResponse(output)

def details(request, team):
    try:
        # obtain the task with the passed id.
        submission = Submission.objects.get(team=team)
    except:
        # respond with a 404 error message
        return HttpResponse(status=404)  
    if(request.method == 'PUT'):
        # parse the incoming information
        data = JSONParser().parse(request)  
        # instanciate with the serializer
        serializer = SubmissionSerializer(submission, data=data)
        # check whether the sent information is okay
        if(serializer.is_valid()):  
            # if okay, save it on the database
            serializer.save() 
            # provide a JSON response with the data that was submitted
            return JsonResponse(serializer.data, status=201)
        # provide a JSON response with the necessary error information
        return JsonResponse(serializer.errors, status=400)
    elif(request.method == 'DELETE'):
        # delete the task
        submission.delete() 
        # return a no content response.
        return HttpResponse(status=204)
    else:
        return HttpResponse("Your team name is: %s"  % submission)
