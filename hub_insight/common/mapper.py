from rest_framework import serializers

from .models import TypeChoices


MAP_JOB_TYPE_TO_PYTHON_TYPE = {
    TypeChoices.interger: int,
    TypeChoices.string: str,
    TypeChoices.float: float,
    TypeChoices.boolean: bool
}


MAP_JOB_TYPE_TO_SERIALIZER = {
    TypeChoices.interger: serializers.IntegerField,
    TypeChoices.string: serializers.CharField,
    TypeChoices.float: serializers.FloatField,
    TypeChoices.boolean: serializers.BooleanField,
}