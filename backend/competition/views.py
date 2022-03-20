import uuid

from django.db.transaction import atomic
from rest_framework import viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from competition.models import Competition
from competition.serializer import CompetitionSerializer
from competitor.serializer import CompetitorSerializer, TeamSerializer
from task.models import SetupTask
from task.serializer import SetupTaskSerializer


class CompetitionViewset(viewsets.ModelViewSet):
    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        with atomic():
            create_serailizer = self.get_serializer(data=request.data)
            create_serailizer.is_valid(raise_exception=True)
            competition_instance = create_serailizer.save()
            self.create_setup_task(competition_instance.id, request_data=request.data)

            competitor_info = request.FILES.get('competitor_info')
            if not competitor_info:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            self.load_competitors(competitor_info, competition_instance)

        return Response(status=status.HTTP_201_CREATED, data=create_serailizer.data)

    def update(self, request, *args, **kwargs):
        competition_id = kwargs.get('pk')
        competition_instance = Competition.objects.get(pk=competition_id)

        with atomic():
            update_serializer = self.get_serializer(competition_instance, data=request.data)
            update_serializer.is_valid(raise_exception=True)
            update_serializer.save()
            self.create_setup_task(competition_instance.id, request_data=request.data)

            competitor_info = request.FILES.get('competitor_info')
            if not competitor_info:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            self.load_competitors(competitor_info, competition_instance)

        return Response(status=status.HTTP_200_OK, data=update_serializer.data)

    def create_setup_task(self, competition_id, request_data):
        # create setup tasks
        private_create_task_serializer = SetupTaskSerializer(data={
            'sql': request_data.get("private_sql"),
            'setup_type': SetupTask.SetupTaskType.PRIVATE_CREATE,
            'competition': competition_id,
        })
        private_create_task_serializer.is_valid(raise_exception=True)
        private_create_task = private_create_task_serializer.save()

        private_query_task_serializer = SetupTaskSerializer(data={
            'sql': request_data.get("reference_query"),
            'setup_type': SetupTask.SetupTaskType.PRIVATE_QUERY,
            'previous_task': private_create_task.id,
            'competition': competition_id,
        })
        private_query_task_serializer.is_valid(raise_exception=True)
        private_query_task_serializer.save()

        public_create_task_serializer = SetupTaskSerializer(data={
            'sql': request_data.get("public_sql"),
            'setup_type': SetupTask.SetupTaskType.PUBLIC_CREATE,
            'competition': competition_id,
        })
        public_create_task_serializer.is_valid(raise_exception=True)
        public_create_task = public_create_task_serializer.save()

        public_query_task_serializer = SetupTaskSerializer(data={
            'sql': request_data.get("reference_query"),
            'setup_type': SetupTask.SetupTaskType.PUBLIC_QUERY,
            'previous_task': public_create_task.id,
            'competition': competition_id,
        })
        public_query_task_serializer.is_valid(raise_exception=True)
        public_query_task_serializer.save()

    def load_competitors(self, competitor_info, competition):
        for line in competitor_info:
            email = line.split()[0].decode()
            username = email.split("@")[0]

            team_data = {
                "uuid": str(uuid.uuid5(uuid.NAMESPACE_DNS, email)),
                "name": username,
                "remain_upload_times": competition.upload_limit,
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


