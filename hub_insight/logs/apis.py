from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema

from hub_insight.common.serializers import PaginationFilterSerializer
from hub_insight.api.pagination import get_paginated_response
from hub_insight.api.mixins import ApiAuthMixin

from .selectors import get_task_log_list
from .serializers import (
    OutputLogTaskListSerializer,
    OutputLogTaskListSwaggerSerializer,
)


class ListLogTaskApi(ApiAuthMixin, APIView):

    @extend_schema(
        tags=["Logs"],
        responses=OutputLogTaskListSwaggerSerializer,
        parameters=[PaginationFilterSerializer]
    )
    def get(self, request):
        
        queryset = get_task_log_list(user=request.user)

        return get_paginated_response(
            serializer_class=OutputLogTaskListSerializer,
            queryset=queryset,
            request=request,
            view=self
        )



