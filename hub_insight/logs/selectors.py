from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _

from rest_framework.exceptions import NotFound

from hub_insight.tasks.models import LogTask
from hub_insight.users.models import User 


# TODO: add filter here
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

    if not user:
        qs = LogTask.objects.all()
    else:
        qs = LogTask.objects.filter(task__user=user)
    

    return qs


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




