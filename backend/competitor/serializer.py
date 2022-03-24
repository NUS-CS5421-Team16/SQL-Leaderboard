from rest_framework import serializers
from rest_framework.fields import ReadOnlyField
from rest_framework.validators import UniqueValidator

from competitor.models import Competitor, Team

from task.serializer import QueryTaskSerializer


class TeamSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=128, validators=[UniqueValidator(queryset=Team.objects.all())])
    status = ReadOnlyField(source='best_public_task.status')
    start_time = ReadOnlyField(source='best_public_task.start_time')
    running_time = ReadOnlyField(source='best_public_task.result')

    class Meta:
        model = Team
        # fields = '__all__'
        fields = ['id', 'status', 'start_time', 'running_time', 'name', 'entry']


class CompetitorSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150, validators=[UniqueValidator(queryset=Competitor.objects.all())])
    email = serializers.EmailField(validators=[UniqueValidator(queryset=Competitor.objects.all())])

    class Meta:
        model = Competitor
        fields = ['username', 'email', 'competition', 'team']

    def create(self, validated_data):
        return super(CompetitorSerializer, self).create(validated_data)

    def update(self, instance, validate_data):
        return super(CompetitorSerializer, self).update(instance, validate_data)