from django.db.models import QuerySet

from hub_insight.tasks.models import LogTask
from hub_insight.users.models import User 


# TODO: add filter here
def get_task_log_list(user:User|None,
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
        qs = LogTask.objects.filter(user=user)
    

    return qs




