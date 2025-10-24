from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from drf_spectacular.utils import extend_schema


from hub_insight.api.mixins import ApiAuthMixin
from hub_insight.api.pagination import get_paginated_response
from .serializers import (
    InputCreateTaskSerializer,
    OutputTaskSerializer,
    OutputTaskSwaggerSerializer
)

from .services import create_task
from .selectors import get_list_of_task
from hub_insight.common.serializers import PaginationFilterSerializer


class CreateListScheduleTaskApi(ApiAuthMixin, APIView):

    @extend_schema(
        tags=["Task"],
        request=InputCreateTaskSerializer,
        responses=OutputTaskSerializer
    )
    def post(self, request):
        
        serializer = InputCreateTaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)


        task = create_task(user=request.user,
                    **serializer.validated_data)

        output_serializer = OutputTaskSerializer(task)

        return Response(output_serializer.data, status.HTTP_201_CREATED)


    @extend_schema(
        tags=["Task"],
        responses=OutputTaskSwaggerSerializer,
        parameters=[PaginationFilterSerializer]
    )
    def get(self, request):
        
        queryset = get_list_of_task(user=request.user)

        return get_paginated_response(
            serializer_class=OutputTaskSerializer,
            queryset=queryset,
            request=request,
            view=self
        )


