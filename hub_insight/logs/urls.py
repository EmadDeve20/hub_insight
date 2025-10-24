from django.urls import path

from .apis import ListLogTaskApi, RetrieveLogTaskApi

name = "logs"

urlpatterns = [
    path("task-log-list/", ListLogTaskApi.as_view(),
        name="get_list_of_task_logs"),

    path("task-log/<int:id>/", RetrieveLogTaskApi.as_view(),
        name="retrieve_task_logs"),
]

