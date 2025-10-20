from django.db import models

from hub_insight.common.models import BaseModel


class Job(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    help = models.CharField(max_length=255)
    script_filename = models.CharField(max_length=255, default="test.py")
    version = models.CharField(max_length=255, default="v1")


    def __str__(self):
        return self.name


