from django.utils.translation import gettext_lazy as _
from django.db.models import QuerySet

from rest_framework.exceptions import NotFound

from hub_insight.users.models import User

from .models import Task


def get_task_by_name(name:str) -> Task:
    """
    get task by name

    Args:
        name (str): name if task

    Raises:
        NotFound: raise not found if task does not exist

    Returns:
        Task: return selected Task object
    """

    try:
        return Task.objects.get(name=name)
    except Task.DoesNotExist:
        raise NotFound(_("task does not exist!"))



# TODO: add filter dict
def get_list_of_task(filter:dict={},
user:User|None = None) -> QuerySet[Task]:
    """
    get list of tasks

    Args:
        filter (dict, optional): filter fields. Defaults to {}.
        user (User | None, optional): user for filter by user. Defaults to None.
        if this is None, this is will be all of tasks.

    Returns:
        QuerySet[Task]: return selected queryset of task
    """

    if not user or user.is_superuser:
        qs = Task.objects.all()

    elif user or not user.is_superuser:
        qs = Task.objects.filter(user=user)

    return qs



