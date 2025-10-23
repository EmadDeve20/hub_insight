from rest_framework.views import APIView
from rest_framework.response import Response


from drf_spectacular.utils import extend_schema


from hub_insight.api.mixins import ApiAuthMixin
from .serializers import InputCreateTaskSerializer

class CreateListScheduleTaskApi(ApiAuthMixin, APIView):

    # TODO: add service  to create task 
    @extend_schema(
        tags=["Task"],
        request=InputCreateTaskSerializer
    )
    def post(self, request):
        
        serializer = InputCreateTaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        print(serializer.validated_data)


        return Response()


