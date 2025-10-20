from django.urls import path

from .apis import GetListJobApi

app_name = "jobs"

urlpatterns = [
    path("", GetListJobApi.as_view(), name="job_list")
]

