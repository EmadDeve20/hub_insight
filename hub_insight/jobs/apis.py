from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema

from hub_insight.api.mixins import ApiAuthMixin
from hub_insight.api.pagination import get_paginated_response
from hub_insight.common.serializers import PaginationFilterSerializer

from .serializers import (
    OutputJobSerializer,
    OutputJobSwaggerSerializer,
)
from .selectors import get_list_job

class GetListJobApi(ApiAuthMixin, APIView):
    
    @extend_schema(
        tags=["Jobs"],
        responses=OutputJobSwaggerSerializer,
        parameters=[PaginationFilterSerializer]
    )
    def get(self, request):
        
        jobs = get_list_job()

        return get_paginated_response(
            serializer_class=OutputJobSerializer,
            queryset=jobs,
            request=request,
            view=self
        )



