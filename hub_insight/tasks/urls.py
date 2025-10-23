from django.urls import path

from .apis import CreateListScheduleTaskApi

app_name = "tasks"

urlpatterns = [
    path("", CreateListScheduleTaskApi.as_view(), name="create_list_schedule_task"),
]