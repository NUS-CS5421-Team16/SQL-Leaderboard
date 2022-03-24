from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from competitor.models import Competitor, Team
from competitor.serializer import CompetitorSerializer, TeamSerializer

from task.serializer import QueryTaskSerializer


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
    def team(self, request, *args, **kwargs):
        # change team detail
        try:
            competitor = Competitor.objects.get(pk=kwargs.get('pk'))
            current_team = competitor.team
            current_team_uuid = competitor.team.uuid
            target_team_uuid = request.data['team_uuid']
            target_team = Team.objects.get(uuid=target_team_uuid)
            if current_team_uuid == target_team_uuid and str(current_team.name) != str(request.data['team_name']):
                Team.objects.filter(uuid=target_team_uuid).update(name=request.data['team_name'])
                # print("[Update Team Name] ", target_team.name, " -> ", request.data['team_name'])
            elif current_team_uuid != target_team_uuid and target_team.name == request.data['team_name']:
                competitor.team = target_team
                competitor.save()
                current_team.delete()
                # print("[Combine Teams] ", current_team.name, " -> ", target_team.name)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST,
                                data={"message": "Please check the uuid or team name"})
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={"message": f"Please check the uuid or team name. ERROR: {str(e)}"})

        json_data = {'id': target_team.id,
                     'name': competitor.username,
                     'team_uuid': target_team.uuid,
                     'team_name': request.data['team_name']
                     }
        if target_team.best_public_task is not None:
            task_serializer = QueryTaskSerializer(target_team.best_public_task)
            json_data['best_public_task'] = task_serializer.data
        else:
            json_data['best_public_task'] = {}
        json_data['remain_upload_times'] = target_team.remain_upload_times

        return Response(status=status.HTTP_200_OK, data=json_data)

    @action(detail=True, methods=['POST', 'GET'])
    def task(self, request, *args, **kwargs):
        # create task
        if request.method == 'POST':

            return Response(status=status.HTTP_200_OK, data={})
        # retrieve latest task of the team
        elif request.method == 'GET':

            return Response(status=status.HTTP_200_OK, data={})
