from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from competitor.models import Competitor, Team
from competitor.serializer import CompetitorSerializer


@api_view(['POST'])
def register(request):
    # change email and password
    email = request.data.get("email")
    if not User.objects.filter(email=email).exists():
        return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "unknown email"})
    name = request.data.get("name")
    password = request.data.get('password')
    user = User.objects.get(email=email)
    if user.password == "":
        competitor = Competitor.objects.filter(email=email).first()
        user.username = name
        user.set_password(password)
        user.save()
        return Response(status=status.HTTP_200_OK, data={"id": user.id,
                                                         "name": user.username,
                                                         "team_uuid": competitor.team.uuid,
                                                         "team_name": competitor.team.name,
                                                         "email": user.email,
                                                         "token": str(user.auth_token),
                                                         "remain_upload_times": competitor.team.remain_upload_times})
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "already registered!"})


@api_view(['POST'])
def login(request):
    # authenticate
    email = request.data.get("email")
    if not User.objects.filter(email=email).exists():
        return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "unknown email"})
    username = User.objects.filter(email=email).first().username
    competitor = Competitor.objects.filter(email=email).first()
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        if not user.is_superuser:
            return Response(status=status.HTTP_200_OK, data={"id": user.id,
                                                             "role": "competitor",
                                                             "name": user.username,
                                                             "team_uuid": competitor.team.uuid,
                                                             "team_name": competitor.team.name,
                                                             "email": user.email,
                                                             "token": str(user.auth_token),
                                                             "remain_upload_times": competitor.team.remain_upload_times})
        if not Token.objects.filter(user=user).exists():
            Token.objects.create(user=user)
        return Response(status=status.HTTP_200_OK, data={"id": user.id,
                                                         "role": "administrator",
                                                         "name": user.username,
                                                         "email": user.email,
                                                         "token": str(user.auth_token)})
    return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "wrong password!"})


class CompetitorViewset(viewsets.ModelViewSet):
    queryset = Competitor.objects.all()
    serializer_class = CompetitorSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        return super(CompetitorViewset, self).retrieve(request, *args, **kwargs)

    @action(detail=True, methods=['PUT'])
    def team(self, request, *args, **kwargs):
        # change team detail

        return Response(status=status.HTTP_200_OK, data={})

    @action(detail=True, methods=['POST', 'GET'])
    def task(self, request, *args, **kwargs):
        # create task
        if request.method == 'POST':

            return Response(status=status.HTTP_200_OK, data={})
        # retrieve latest task of the team
        elif request.method == 'GET':

            return Response(status=status.HTTP_200_OK, data={})
