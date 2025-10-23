from rest_framework.views import APIView
from rest_framework.response import Response


from drf_spectacular.utils import extend_schema


from hub_insight.api.mixins import ApiAuthMixin
from .serializers import InputCreateTaskSerializer
from .services import create_task

class CreateListScheduleTaskApi(ApiAuthMixin, APIView):

    # TODO: add service  to create task 
    @extend_schema(
        tags=["Task"],
        request=InputCreateTaskSerializer
    )
    def post(self, request):
        
        serializer = InputCreateTaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)


        task = create_task(user=request.user,
                    **serializer.validated_data)

        print(f"{task=}")

        return Response()


