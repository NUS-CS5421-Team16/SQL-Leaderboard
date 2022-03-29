from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from competitor.models import Competitor, Team, Competition
from competitor.serializer import CompetitorSerializer
from task.models import QueryTask
from task.serializer import QueryTaskSerializer
from task.tasks import async_run_task


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
        # check permission
        user_id = int(kwargs.get("pk"))
        if not request.user.is_superuser and request.user.id != user_id:
            return Response(status=status.HTTP_401_UNAUTHORIZED, data={"message": "permission denied!"})

        competitor_instance = Competitor.objects.get(id=user_id)

        team = competitor_instance.team
        tasks = QueryTask.objects.filter(competitor__team=team).order_by("start_time")
        tasks_serializer = QueryTaskSerializer(tasks, many=True)
        latest_task_serializer = QueryTaskSerializer(tasks.first())

        result_data = {
            "id": competitor_instance.id,
            "name": request.user.username,
            "team_uuid": competitor_instance.team.uuid,
            "team_name": competitor_instance.team.name,
            "latest_task": latest_task_serializer.data,
            "tasks": tasks_serializer.data,
            "remain_upload_times": team.remain_upload_times
        }
        return Response(status=status.HTTP_200_OK, data=result_data)

    @action(detail=True, methods=['PUT'])
    def team(self, request, *args, **kwargs):
        # check permission
        user_id = int(kwargs.get("pk"))
        if not request.user.is_superuser and request.user.id != user_id:
            return Response(status=status.HTTP_401_UNAUTHORIZED, data={"message": "permission denied!"})

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
                is_desc = Competition.objects.first().descendent_ordering
                if current_team.best_public_task is not None:
                    if target_team.best_public_task is None:
                        target_team.best_public_task = current_team.best_public_task
                    elif is_desc and target_team.best_public_task.result < current_team.best_public_task.result:
                        target_team.best_public_task = current_team.best_public_task
                    elif not is_desc and target_team.best_public_task.result > current_team.best_public_task.result:
                        target_team.best_public_task = current_team.best_public_task
                target_team.remain_upload_times = max(target_team.remain_upload_times, current_team.remain_upload_times)
                target_team.entries = target_team.entries + current_team.entries
                target_team.save()
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
        # check permission
        user_id = int(kwargs.get("pk"))
        if not request.user.is_superuser and request.user.id != user_id:
            return Response(status=status.HTTP_401_UNAUTHORIZED, data={"message": "permission denied!"})

        # create task
        if request.method == 'POST':
            # check remain_upload_times
            competitor_instance = Competitor.objects.get(pk=user_id)
            remain_upload_times = competitor_instance.team.remain_upload_times
            if remain_upload_times > 0:
                competitor_instance.team.remain_upload_times = remain_upload_times - 1
                competitor_instance.team.entries += 1
                competitor_instance.team.save()
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "You are not allowed to upload "
                                                                                     "today, please upload after "
                                                                                     "12:00am"})
            # check ddl
            competition_deadline = competitor_instance.competition.end_time
            if competition_deadline < timezone.now():
                return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "Competition ended! You are not "
                                                                                     "allowed to upload sql any more!"})

            # check if there are any dangerous operations
            sql_file = request.FILES.get('sql')
            sql = sql_file.read().decode()
            for op in QueryTask.dangerous_ops:
                if sql.find(op) != -1:
                    return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "Write operation detected! "
                                                                                         "Only SELECT is allowed"})
            # create query task
            serializer = QueryTaskSerializer(data={
                "sql": sql_file,
                "query_type": QueryTask.QueryTaskType.PUBLIC,
                "competitor": user_id
            })
            serializer.is_valid(raise_exception=True)
            querytask = serializer.save()

            # run task
            async_run_task.apply_async((querytask.id, "querytask"))
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)
        # retrieve latest task of the team
        elif request.method == 'GET':
            competitor_instance = Competitor.objects.get(pk=user_id)
            team = competitor_instance.team
            task = QueryTask.objects.filter(competitor__team=team).order_by("-start_time").first()
            task_serializer = QueryTaskSerializer(task)
            return Response(status=status.HTTP_200_OK, data=task_serializer.data)
