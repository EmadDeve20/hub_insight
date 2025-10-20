from django.urls import path, include

urlpatterns = [
    path('v1/users/', include(('hub_insight.users.urls', 'users'))),
    path('v1/jobs/', include(('hub_insight.jobs.urls', 'jobs'))),
]
