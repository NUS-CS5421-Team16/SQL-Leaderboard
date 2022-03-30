import uuid
from rest_framework import serializers

from competition.models import Competition


class CompetitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competition
        exclude = ['private_result', 'public_result']

