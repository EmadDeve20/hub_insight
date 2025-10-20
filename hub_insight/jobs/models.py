from django.db import models

from hub_insight.common.models import BaseModel


class Job(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    help = models.CharField(max_length=255)


