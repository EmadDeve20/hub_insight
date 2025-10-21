from rest_framework  import serializers

from .models import Job, Variable, Response, TypeChoices

from hub_insight.common.serializers import SwaggerListSerializer


class OutputJobVariablesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Variable
        fields = [
            "name",
            "var_type",
            "default",
        ]


class  OutputJobResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response
        fields = [
            "response_type",
        ]


class OutputJobSerializer(serializers.ModelSerializer):

    variables = OutputJobVariablesSerializer(many=True, read_only=True)
    response_type = serializers.ChoiceField(choices=TypeChoices.choices,
                                            source='response_type.response_type',
                                            read_only=True)

    class Meta:
        model = Job
        fields = [
            "id",
            "name",
            "help",
            "variables",
            "response_type",
        ]


class OutputJobSwaggerSerializer(SwaggerListSerializer):
    results = serializers.ListField(child=OutputJobSerializer())


