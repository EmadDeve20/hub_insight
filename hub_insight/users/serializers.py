from django.utils.translation import gettext_lazy as _

from .models import User

from rest_framework import serializers


class InputCreateUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255) 
    first_name = serializers.CharField(max_length=255) 
    last_name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    password = serializers.CharField()
    confirm_password = serializers.CharField()

    def username_validate(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(_("this username used befor for another user!"))

        return username

    def email_validate(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(_("this email used befor for another user!"))

        return email

    def validate(self, attrs):

        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")

        if password != confirm_password:
            raise serializers.ValidationError(_("password and confirm password are not same!"))

        return attrs


class OutputUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "username",
            "created_at"
        ]


