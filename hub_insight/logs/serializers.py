from rest_framework import serializers

from hub_insight.common.serializers import SwaggerListSerializer
from hub_insight.tasks.models import LogTask

class OutputLogTaskListSerializer(serializers.ModelSerializer):

    job = serializers.CharField(source="task.job.name", default=None)

    class Meta:
        model = LogTask
        fields = [
            "id",
            "created_at",
            "job",
            "is_ok",
            "variables"
        ]


class OutputLogTaskListSwaggerSerializer(SwaggerListSerializer):
    results = serializers.ListField(child=OutputLogTaskListSerializer())

