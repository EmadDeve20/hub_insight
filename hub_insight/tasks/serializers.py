
from django_celery_beat.validators import crontab_validator

from rest_framework import serializers

from hub_insight.jobs.selectors import get_job_by_id
from hub_insight.common.mapper import MAP_JOB_TYPE_TO_SERIALIZER as MAP_SERIALIZER
from hub_insight.common.mapper import MAP_JOB_TYPE_TO_PYTHON_TYPE as MAP_PYTHON

from .models import Task
from hub_insight.jobs.serializers import OutputJobSerializer
from hub_insight.users.serializers import OutputUserSerializer
from hub_insight.common.serializers import SwaggerListSerializer


def generate_variables_serializer(job_id:int) -> serializers.Serializer|None:
    """
    get job id and return serializer for variables of job.

    Args:
        job_id (int): job id

    Returns:
        serializers.Serializer|None: return a Serializer class if job has variables.
        otherwise, retrurn None 
    """

    fields_dict = {}

    job = get_job_by_id(job_id)
    
    for var in job.variables.all():
        if var.default:
            fields_dict[var.name] = MAP_SERIALIZER[var.var_type](default=MAP_PYTHON[var.var_type](var.default)) 
        else:
            fields_dict[var.name] = MAP_SERIALIZER[var.var_type]() 

    if not fields_dict:
        return None

    DymanicSerializer = type("DynamicSerializer", (serializers.Serializer,), fields_dict)

    return DymanicSerializer



class InputCreateTaskSerializer(serializers.Serializer):
    job_id = serializers.IntegerField()
    cron_expression = serializers.CharField(default="* * * * *", validators=[crontab_validator])
    variables = serializers.JSONField()
    enabled = serializers.BooleanField(default=True)


    def validate(self, attrs):
        job_id =  attrs["job_id"]
        variables = attrs["variables"]

        variables_serializer = generate_variables_serializer(job_id=job_id)
        
        if variables_serializer:
            variables = variables_serializer(data=variables)
            variables.is_valid(raise_exception=True)
            variables = variables.validated_data
        else:
            variables = {}
        
        attrs["variables"] = variables
        

        return attrs


class OutputTaskSerializer(serializers.ModelSerializer):

    user = OutputUserSerializer()
    job = OutputJobSerializer()

    class Meta:
        model = Task
        fields = [
            "id",
            "user",
            "job",
            "enabled",
            "variables",
            "created_at",
        ]


class OutputTaskSwaggerSerializer(SwaggerListSerializer):
    results = serializers.ListField(child=OutputTaskSerializer())

