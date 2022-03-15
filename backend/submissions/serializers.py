from rest_framework import routers,serializers,viewsets
from .models import Submission
class SubmissionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Submission
        fields = ['team', 'scores', 'times', 'time_stamp']