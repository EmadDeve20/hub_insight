from django.utils.translation import gettext_lazy as _

from rest_framework.exceptions import NotFound

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


