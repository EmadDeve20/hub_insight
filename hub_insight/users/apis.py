from hub_insight.api.mixins import ApiAuthMixin

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .permissions import CreateUserPermission

from .services import create_user
from .serializers import (
    InputCreateUserSerializer,
    OutputUserSerializer
)

from drf_spectacular.utils import extend_schema


class CreateUserApi(ApiAuthMixin, APIView):
    permission_classes = [IsAuthenticated, CreateUserPermission]

    @extend_schema(
        tags=["Users"],
        request=InputCreateUserSerializer,
        responses=OutputUserSerializer
    )
    def post(self, request):
        
        serializer = InputCreateUserSerializer(data=request.data)
        
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        data.pop("confirm_password")

        user = create_user(**data)

        output_serializer = OutputUserSerializer(user)

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
    
