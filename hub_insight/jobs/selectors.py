from django.db.models import QuerySet

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



