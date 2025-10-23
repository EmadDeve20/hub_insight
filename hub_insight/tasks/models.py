from django.db import models

from hub_insight.common.models import BaseModel

from django_celery_beat.models import PeriodicTask, CrontabSchedule



class Task(BaseModel):
    name = models.CharField(max_length=255)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    job = models.ForeignKey("jobs.Job", on_delete=models.CASCADE)
    enabled = models.BooleanField(default=True)
    celery_periodic_task = models.ForeignKey(PeriodicTask,
                                             on_delete=models.CASCADE,
                                             related_name='custom_task_periodic',)
    celery_cron_schedule = models.ForeignKey(CrontabSchedule,
                                             on_delete=models.CASCADE,
                                             related_name='custom_task_crontab')
    variables = models.JSONField()


    def save(self, *args, **kwarfg):
        self.celery_periodic_task.enabled = self.enabled
        
        self.celery_periodic_task.save()

        return super().save(*args, **kwarfg)


    def delete(self, *args, **kwarfg):
        self.celery_periodic_task.delete()

        return super().delete(*args, **kwarfg)


