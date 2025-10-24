from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from drf_spectacular.utils import extend_schema


from hub_insight.api.mixins import ApiAuthMixin
from hub_insight.api.pagination import get_paginated_response
from .serializers import (
    InputCreateTaskSerializer,
    OutputTaskSerializer,
    OutputTaskSwaggerSerializer,
    InputPatchTaskSerializer
)

from .services import (
    create_task,
    delete_task_by_id,
    partial_update_task_by_id
)

from .selectors import (
    get_list_of_task,
    get_task_by_id,
)

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



class UpdateDeleteRetriveTaskApi(ApiAuthMixin, APIView):

    @extend_schema(
        tags=["Task"],
        responses=OutputTaskSerializer
    )
    def get(self, request, id):
        
        task = get_task_by_id(task_id=id, user=request.user)

        output_seirlaizer = OutputTaskSerializer(task)

        return Response(output_seirlaizer.data)


    @extend_schema(
        tags=["Task"],
        request=InputPatchTaskSerializer,
        responses=OutputTaskSerializer
    )
    def patch(self, request, id):
        
        serializer = InputPatchTaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        updated_task = partial_update_task_by_id(task_id=id,
                                                 user=request.user,
                                                 **serializer.validated_data)
        
        output_serializer = OutputTaskSerializer(updated_task)

        return Response(output_serializer.data)


    @extend_schema(
        tags=["Task"],
    )
    def delete(self, request, id):
        
        delete_task_by_id(task_id=id, user=request.user)

        return Response(status=status.HTTP_204_NO_CONTENT)





