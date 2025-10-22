from rest_framework.views import APIView
from rest_framework import serializers

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
    
    class InputArgSerializer(serializers.Serializer):
        search = serializers.CharField(required=False,
                                       help_text="search on fields: name, help, variables__name")

    @extend_schema(
        tags=["Jobs"],
        responses=OutputJobSwaggerSerializer,
        parameters=[PaginationFilterSerializer, InputArgSerializer]
    )
    def get(self, request):
        
        filter_serializer = self.InputArgSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)

        jobs = get_list_job(filter_serializer.validated_data)

        return get_paginated_response(
            serializer_class=OutputJobSerializer,
            queryset=jobs,
            request=request,
            view=self
        )



