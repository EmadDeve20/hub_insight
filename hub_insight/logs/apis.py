from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers

from drf_spectacular.utils import extend_schema

from hub_insight.common.serializers import PaginationFilterSerializer
from hub_insight.api.pagination import get_paginated_response
from hub_insight.api.mixins import ApiAuthMixin

from .selectors import (
    get_task_log_list,
    get_task_log_by_id,
)

from .serializers import (
    OutputLogTaskListSerializer,
    OutputLogTaskListSwaggerSerializer,
    OutputRetrieveLogTaskSerializer
)


class ListLogTaskApi(ApiAuthMixin, APIView):

    class InputArgSerializer(serializers.Serializer):
        search = serializers.CharField(required=False,
                                       help_text="search on fields: job,")
        
        boolean_choices = ("true", "false")

        is_enabled = serializers.ChoiceField(required=False, choices=boolean_choices)
        job_ids = serializers.CharField(required=False, help_text="id of jobs. seprated by ,")
        user_ids = serializers.CharField(required=False, help_text="id of users. seprated by ,")
        order_by = serializers.CharField(required=False, help_text="order by response fields."
                                         "for example order by jobs name: `job__name`"
                                         " or reverse: `-job__name`. you can use more seprated by `,`")
        is_ok = serializers.ChoiceField(required=False, choices=boolean_choices)


    @extend_schema(
        tags=["Logs"],
        responses=OutputLogTaskListSwaggerSerializer,
        parameters=[PaginationFilterSerializer, InputArgSerializer]
    )
    def get(self, request):
        
        filter_serializer = self.InputArgSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)

        queryset = get_task_log_list(user=request.user,
                                     filter=filter_serializer.validated_data)

        return get_paginated_response(
            serializer_class=OutputLogTaskListSerializer,
            queryset=queryset,
            request=request,
            view=self
        )


class RetrieveLogTaskApi(ApiAuthMixin, APIView):

    @extend_schema(
        tags=["Logs"],
        responses=OutputRetrieveLogTaskSerializer,
    )
    def get(self, request, id):

        log = get_task_log_by_id(task_log_id=id, user=request.user)

        
        output_serializer = OutputRetrieveLogTaskSerializer(log)

        return Response(output_serializer.data)

