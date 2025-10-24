from django.db import models

from hub_insight.common.models import BaseModel, TypeChoices

from django_celery_beat.models import PeriodicTask



class Task(BaseModel):
    name = models.CharField(max_length=255, unique=True, editable=False)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    job = models.ForeignKey("jobs.Job", on_delete=models.CASCADE)
    enabled = models.BooleanField(default=True)
    celery_periodic_task = models.ForeignKey(PeriodicTask,
                                             on_delete=models.CASCADE,
                                             related_name='custom_task_periodic',)

    variables = models.JSONField()


    def save(self, *args, **kwarfg):
        self.celery_periodic_task.enabled = self.enabled
        
        self.celery_periodic_task.save()

        return super().save(*args, **kwarfg)


    def delete(self, *args, **kwarfg):
        self.celery_periodic_task.delete()

        return super().delete(*args, **kwarfg)



class LogTask(BaseModel):
    task = models.ForeignKey(Task, on_delete=models.SET_NULL,
                             related_name="logs",
                             null=True)

    is_ok = models.BooleanField(default=True)
    error_message = models.CharField(max_length=255,
                                     null=True,
                                     default=None)
    
    # I wana to save variables and help default jobs because
    # job can be updated to another version and maybe variables and help changed.
    variables = models.JSONField()
    job_help = models.TextField()

    response_type = models.CharField(max_length=255,
                                choices=TypeChoices.choices,
                                )

    response_value = models.TextField()
    job_version = models.CharField(max_length=255, default="v1")

    class Meta:
        indexes = [
            models.Index(fields=['task', 'created_at']),
            models.Index(fields=['is_ok']),
        ]

