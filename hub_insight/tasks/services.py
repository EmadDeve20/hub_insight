import json

from uuid import uuid4

from config.django.base import MAXIMUM_ENABLED_JOB

from django.db import transaction
from django_celery_beat.models import CrontabSchedule
from django.utils.translation import gettext_lazy as txt_lazy

from rest_framework.exceptions import ValidationError

from .models import (
    Task,
    PeriodicTask,
    LogTask,
)

from hub_insight.jobs.selectors import get_job_by_id

from hub_insight.users.models import User

@transaction.atomic
def create_task(user:User,
job_id:int, cron_expression:str, variables:dict, enabled:bool=True) -> Task:
    """
    create a tast

    Args:
        user (User): user requester
        job_id (int): job id
        cron_expression (str): valid cron expression 
        variables (dict): variables
        enabled (bool): default is True

    Returns:
        Task: retuern created task
    """

    # check permission for user has permission to make more task or not?
    # for example, here we just check user is suepruser or not 
    # we set a permission and check by it like this:
    # user.has_perm('tasks.add_more_task')

    if enabled and not user.is_superuser:
        if Task.objects.filter(user=user, enabled=True).count() >= MAXIMUM_ENABLED_JOB:
            raise ValidationError(txt_lazy("you cannot have enabled task "
                                    "more than %(maximum_en)s") 
                                    % {"maximum_en": str(MAXIMUM_ENABLED_JOB)})


    cron_expression = cron_expression.split()
    
    job = get_job_by_id(job_id)

    cron , _= CrontabSchedule.objects.get_or_create(
        minute=cron_expression[0],
        hour=cron_expression[1],
        day_of_week=cron_expression[2],
        day_of_month=cron_expression[3],
        month_of_year=cron_expression[4]
    )

    task_name = f"{user.username}_{uuid4()}_{job.id}"

    periodic_task = PeriodicTask.objects.create(
        name=task_name,
        task="hub_insight.tasks.tasks.run_job_task",
        args=json.dumps([task_name]),
        crontab=cron,
        enabled=enabled
    )


    return Task.objects.create(
        name=task_name,
        user=user,
        job=job,
        celery_periodic_task=periodic_task,
        variables=variables,
        enabled=enabled
    )



@transaction.atomic
def create_task_log(task:Task, response_value:str,
response_type:str, variables:dict, job_help:str, job_version:str,
is_ok:bool=True, error_message:str|None=None) -> LogTask:
    """
    create log for runned task

    Args:
        task (Task): task object
        response_value (str): response value
        response_type (str): type of response
        variables (dict): runned task with variables
        job_help (str): run time help of default jobs
        job_version(str): version of job

    Returns:
        LogTask: return created LogTask
    """

    return LogTask.objects.create(
        task=task,
        response_value=response_value,
        response_type=response_type,
        variables=variables,
        job_help=job_help,
        job_version=job_version,
        is_ok=is_ok,
        error_message=error_message,
    )


