from django.urls import path

from .apis import (
    CreateListScheduleTaskApi,
    UpdateDeleteRetriveTaskApi,
)

app_name = "tasks"

urlpatterns = [
    path("", CreateListScheduleTaskApi.as_view(),
         name="create_list_task"),
    
    path("<int:id>/", UpdateDeleteRetriveTaskApi.as_view(),
         name="update_delete_retrive_task"),
]