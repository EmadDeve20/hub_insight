from django.db.models import QuerySet

from .models import Job

# TODO: add filter for this selector
def get_list_job(filter:dict={}) -> QuerySet[Job]:
    return Job.objects.all()


