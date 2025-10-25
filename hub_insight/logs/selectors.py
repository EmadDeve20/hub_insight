from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _

from rest_framework.exceptions import NotFound

from hub_insight.tasks.models import LogTask
from hub_insight.users.models import User 

from .filters import TaskLogFilterSet

def get_task_log_list(user:User|None=None,
filter:dict={}) -> QuerySet[LogTask]:
    """
    get list of tasks log

    Args:
        user (User | None, optional): user to filter by a user. Defaults to None.
        filter (dict, optional): filter on fields. Defaults to {}.

    Returns:
        QuerySet[LogTask]: return queryset of LogTask
    """

    if not user or (user and user.is_superuser):
        qs = LogTask.objects.all()

    elif user and not user.is_superuser :
        if filter and "user_ids" in filter:
            filter.pop("user_ids")

        qs = LogTask.objects.filter(task__user=user)
    

    return TaskLogFilterSet(filter, qs).qs


def get_task_log_by_id(task_log_id:int, user:User|None=None) -> LogTask:
    """
    get task log by id

    Args:
        task_log_id (int): id of log
        user (User | None, optional): user to filter by user. Defaults to None.

    Raises:
        NotFound: raise notfound if log does not exist

    Returns:
        LogTask: retrun selected Log object
    """

    try:
        return get_task_log_list(user=user).get(id=task_log_id)
    except  LogTask.DoesNotExist:
        raise NotFound(_("log does not exist!"))




