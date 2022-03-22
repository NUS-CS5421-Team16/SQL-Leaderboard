from rest_framework import serializers

from task.models import SetupTask


class SetupTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SetupTask
        fields = "__all__"

    def create(self, validated_data):
        return super(SetupTaskSerializer, self).create(validated_data)