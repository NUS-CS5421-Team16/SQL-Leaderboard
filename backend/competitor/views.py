from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from django.core import serializers
from rest_framework.decorators import api_view, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from competitor.models import Competitor, Team
from competitor.serializer import CompetitorSerializer, TeamSerializer


@api_view(['POST'])
def register(request):
    # change email and password
    print('register')
    return Response(status=status.HTTP_200_OK, data={})


@api_view(['POST'])
def login(request):
    # authenticate
    print('login')
    return Response(status=status.HTTP_200_OK, data={})


class CompetitorViewset(viewsets.ModelViewSet):
    queryset = Competitor.objects.all()
    serializer_class = CompetitorSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        return super(CompetitorViewset, self).retrieve(request, *args, **kwargs)

    @action(detail=True, methods=['PUT'])
    def team(self, request, pk=None):
        # change team detail
        try:
            competitor = Competitor.objects.get(pk=pk)
            current_team = competitor.team
            current_team_uuid = competitor.team.uuid
            target_team_uuid = request.data['team_uuid']
            target_team = Team.objects.get(uuid=target_team_uuid)
            if current_team_uuid == target_team_uuid and str(current_team.name) != str(request.data['team_name']):
                Team.objects.filter(uuid=target_team_uuid).update(name=request.data['team_name'])
                print("[Update Team Name] ", target_team.name, " -> ", request.data['team_name'])
            elif current_team_uuid != target_team_uuid and target_team.name == request.data['team_name']:
                competitor.team = target_team
                competitor.save()
                current_team.delete()
                print("[Combine Teams] ", current_team.name, " -> ", target_team.name)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={"Please check the uuid or team name"})
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"Please check the uuid or team name"})

        return Response(status=status.HTTP_200_OK, data=serializers.serialize('json', [target_team, ]))

    @action(detail=True, methods=['POST', 'GET'])
    def task(self, request, *args, **kwargs):
        # create task
        if request.method == 'POST':

            return Response(status=status.HTTP_200_OK, data={})
        # retrieve latest task of the team
        elif request.method == 'GET':

            return Response(status=status.HTTP_200_OK, data={})
