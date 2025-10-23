from django.db import models

from hub_insight.common.models import BaseModel

from django_celery_beat.models import PeriodicTask



class ScheduleTask(BaseModel):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    job = models.ForeignKey("jobs.Job", on_delete=models.CASCADE)
    enable = models.BooleanField(default=True)
    celery_periodic_task = models.ForeignKey(PeriodicTask, on_delete=models.CASCADE)
    variables = models.JSONField()


    def save(self, *args, **kwarfg):
        celery_periodic_task.enable = self.enable
        
        celery_periodic_task.save()

        return super().save(*args, **kwarfg)


    def delete(self, *args, **kwarfg):
        celery_periodic_task.delete()

        return super().delete(*args, **kwarfg)


