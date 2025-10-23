from django.urls import path, include

urlpatterns = [
    path('v1/users/', include(('hub_insight.users.urls', 'users'))),
    path('v1/jobs/', include(('hub_insight.jobs.urls', 'jobs'))),
    path('v1/authentication/', include(('hub_insight.authentication.urls', 'authentication'))),
    path('v1/tasks/', include(('hub_insight.tasks.urls', 'tasks'))),
]
