import uuid
from django.utils import timezone

from django.db.transaction import atomic
from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from competition.models import Competition
from competition.serializer import CompetitionSerializer
from competitor.models import Team, Competitor
from competitor.serializer import CompetitorSerializer, TeamSerializer, PublicTeamSerializer, PrivateTeamSerializer

from task.models import SetupTask
from task.serializer import SetupTaskSerializer

from competitor.models import Team
from task.tasks import async_run_task


class CompetitionViewset(viewsets.ModelViewSet):
    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer
    permission_classes = [IsAdminUser]

    def list(self, request, *args, **kwargs):
        instance = Competition.objects.all().first()
        if instance is not None:
            serializer = CompetitionSerializer(instance)
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND, data={"message": "competition not found!"})

    def retrieve(self, request, *args, **kwargs):
        return super(CompetitionViewset, self).retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        # TODO: if have 1 valid competition, skip
        competitions = Competition.objects.all()
        if competitions.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "competition already exists!"})

        with atomic():
            create_serailizer = self.get_serializer(data=request.data)
            create_serailizer.is_valid(raise_exception=True)
            competition_instance = create_serailizer.save()
            setuptask_id_list = self.create_setup_task(competition_instance.id, request_data=request.data)

            competitor_info = request.FILES.get('competitor_info')
            if not competitor_info:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            self.load_competitors(competitor_info, competition_instance)

        self.run_setup_task(setuptask_id_list)

        return Response(status=status.HTTP_201_CREATED, data=create_serailizer.data)

    def update(self, request, *args, **kwargs):
        competition_id = kwargs.get('pk')
        competition_instance = Competition.objects.get(pk=competition_id)

        with atomic():
            self.clear_competition(competition_instance)

            update_serializer = self.get_serializer(competition_instance, data=request.data)
            update_serializer.is_valid(raise_exception=True)
            update_serializer.save()
            setuptask_id_list = self.create_setup_task(competition_instance.id, request_data=request.data)

            competitor_info = request.FILES.get('competitor_info')
            if not competitor_info:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            self.load_competitors(competitor_info, competition_instance)

        self.run_setup_task(setuptask_id_list)

        return Response(status=status.HTTP_200_OK, data=update_serializer.data)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def rank(self, request, *args, **kwargs):
        try:
            is_private = bool(int(request.query_params.get('private')))
            is_desc = bool(int(request.query_params.get('ordering')))
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={"message": f"Please Check the URL. ERROR: {str(e)}"})
        json_data = {}
        if not is_private:
            if is_desc:
                teams = Team.objects.all().order_by('-best_public_task__result', 'entries',
                                                    'best_public_task__start_time')
            else:
                teams = Team.objects.all().order_by('best_public_task__result', 'entries',
                                                    'best_public_task__start_time')
            teams_serializer = PublicTeamSerializer(teams, many=True)
        else:
            competition_deadline = Competition.objects.first().end_time
            if competition_deadline > timezone.now():
                return Response(status=status.HTTP_400_BAD_REQUEST,
                                data={"message": "Cannot check the private leaderboard's results now."})

            if is_desc:
                teams = Team.objects.all().order_by('-best_private_task__result', 'entries',
                                                    'best_private_task__start_time')
            else:
                teams = Team.objects.all().order_by('best_private_task__result', 'entries',
                                                    'best_private_task__start_time')
            teams_serializer = PrivateTeamSerializer(teams, many=True)

        teams_data = teams_serializer.data
        invalid_teams = []
        rank_idx = 1
        for item in teams_data:
            if 'status' not in item or item['status'] != "success":
                invalid_teams.append(item)
            else:
                json_data[rank_idx] = item
                rank_idx += 1
        if len(invalid_teams) > 0:
            json_data[-1] = invalid_teams

        return Response(status=status.HTTP_200_OK, data=json_data)

    @action(methods=['get'], detail=False)
    def download_public(self, *args, **kwargs):
        competitions = Competition.objects.all()
        if not competitions.exists():
            return Response(status=status.HTTP_404_NOT_FOUND, data={"message": "competition not found!"})
        instance = competitions.first()

        # get an open file handle (I'm just using a file attached to the model for this example):
        with instance.private_sql.open('r') as file:
            response = HttpResponse(file, content_type='application/msword')
            response['Content-Disposition'] = 'attachment; filename=public.sql'
            return response

    def create_setup_task(self, competition_id, request_data):
        task_id_list = []
        # create setup tasks
        private_create_task_serializer = SetupTaskSerializer(data={
            'sql': request_data.get("private_sql"),
            'setup_type': SetupTask.SetupTaskType.PRIVATE_CREATE,
            'competition': competition_id,
        })
        private_create_task_serializer.is_valid(raise_exception=True)
        private_create_task = private_create_task_serializer.save()
        task_id_list.append(private_create_task.id)

        private_query_task_serializer = SetupTaskSerializer(data={
            'sql': request_data.get("reference_query"),
            'setup_type': SetupTask.SetupTaskType.PRIVATE_QUERY,
            'previous_task': private_create_task.id,
            'competition': competition_id,
        })
        private_query_task_serializer.is_valid(raise_exception=True)
        private_query_task = private_query_task_serializer.save()
        task_id_list.append(private_query_task.id)

        public_create_task_serializer = SetupTaskSerializer(data={
            'sql': request_data.get("public_sql"),
            'setup_type': SetupTask.SetupTaskType.PUBLIC_CREATE,
            'competition': competition_id,
        })
        public_create_task_serializer.is_valid(raise_exception=True)
        public_create_task = public_create_task_serializer.save()
        task_id_list.append(public_create_task.id)

        public_query_task_serializer = SetupTaskSerializer(data={
            'sql': request_data.get("reference_query"),
            'setup_type': SetupTask.SetupTaskType.PUBLIC_QUERY,
            'previous_task': public_create_task.id,
            'competition': competition_id,
        })
        public_query_task_serializer.is_valid(raise_exception=True)
        public_query_task = public_query_task_serializer.save()
        task_id_list.append(public_query_task.id)

        return task_id_list

    def run_setup_task(self, task_id_list):
        for task_id in task_id_list:
            async_run_task.apply_async((task_id, "setuptask"))

    def load_competitors(self, competitor_info, competition):
        for line in competitor_info:
            email = line.split()[0].decode()
            username = email.split("@")[0]

            team_data = {
                "uuid": str(uuid.uuid5(uuid.NAMESPACE_DNS, email)),
                "name": username,
                "remain_upload_times": competition.upload_limit,
                "entries": 0,
            }
            team_serializer = TeamSerializer(data=team_data)
            team_serializer.is_valid(raise_exception=True)
            team = team_serializer.save()

            competitor_data = {
                "competition": competition.id,
                "team": team.id,
                "email": email,
                "username": username,
            }
            competitor_serializer = CompetitorSerializer(data=competitor_data)
            competitor_serializer.is_valid(raise_exception=True)
            competitor = competitor_serializer.save()

            Token.objects.create(user=competitor)

    def clear_competition(self, instance):
        # delete local files
        instance.competitor_info.delete(False)
        instance.private_sql.delete(False)
        instance.public_sql.delete(False)
        instance.reference_query.delete(False)
        instance.save()

        # delete teams and competitors
        Team.objects.all().delete()
        competitors = Competitor.objects.all().delete()

