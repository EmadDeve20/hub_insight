from django.urls import path, include

urlpatterns = [
    path('users/', include(('hub_insight.users.urls', 'users')))
]
