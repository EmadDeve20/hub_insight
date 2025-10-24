from django.urls import path

from .apis import ListLogTaskApi

name = "logs"

urlpatterns = [
    path("task-log-list/", ListLogTaskApi.as_view(),
        name="get_list_of_task_logs")
]

