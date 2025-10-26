from .models import Task
from django.utils.translation import gettext_lazy as txt_lazy
from config.django.base import MAXIMUM_ENABLED_JOB
from hub_insight.users.models import User
from rest_framework.exceptions import ValidationError

def check_permission_create_enabled_task(user:User):
    # check permission for user has permission to make more task or not?
    # for example, here we just check user is suepruser or not 
    # we set a permission and check by it like this:
    # user.has_perm('tasks.add_more_task')

    if user.is_superuser:
        return True

    if Task.objects.filter(user=user, enabled=True).count() >= MAXIMUM_ENABLED_JOB:
        raise ValidationError(txt_lazy("you cannot have enabled task "
                                "more than %(maximum_en)s") 
                                % {"maximum_en": str(MAXIMUM_ENABLED_JOB)})
    
    return True

