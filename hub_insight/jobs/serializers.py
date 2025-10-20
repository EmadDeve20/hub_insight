from rest_framework  import serializers

from .models import Job

from hub_insight.common.serializers import SwaggerListSerializer

# TODO: add variables and response
class OutputJobSerializer(serializers.ModelSerializer):

    class Meta:
        model = Job
        fields = [
            "id",
            "name",
            "help",
        ]


class OutputJobSwaggerSerializer(SwaggerListSerializer):
    results = serializers.ListField(child=OutputJobSerializer())


