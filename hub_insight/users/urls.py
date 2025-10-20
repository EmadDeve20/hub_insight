from django.urls import path

from .apis import CreateUserApi

app_name = "users"

urlpatterns = [
    path("", CreateUserApi.as_view(), name="create_user")
]

