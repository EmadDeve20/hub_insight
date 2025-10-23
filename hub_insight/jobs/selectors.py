from django.utils.translation import gettext_lazy as _
from django.db.models import QuerySet

from rest_framework.exceptions import NotFound

from .models import Job
from .filters import JobFilterSet


def get_list_job(filter:dict={}) -> QuerySet[Job]:
    """
    get list of jobs

    Args:
        filter (dict, optional): dictionary filters of fields. Defaults to {}.

    Returns:
        QuerySet[Job]: return queryset of Job
    """

    qs = Job.objects.all()

    return JobFilterSet(filter, qs).qs



def get_job_by_id(job_id:int) -> Job:
    """
    get job by id

    Args:
        job_id (int): id of job

    Raises:
        NotFound: raise not found if job is not exist

    Returns:
        Job: return selected job object
    """

    try:
        return Job.objects.get(id=job_id)
    except Job.DoesNotExist:
        raise NotFound(_("job does not exist!"))
    