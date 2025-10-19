from django.db import models
from hub_insight.common.models import BaseModel

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager as BUM
from django.contrib.auth.models import PermissionsMixin




class BaseUserManager(BUM):
    def create_user(self, username, is_active=True,  password=None):
        if not username:
            raise ValueError("Users must have an username")

        user = self.model(username=username, is_active=is_active)

        if password is not None:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.full_clean()
        user.save(using=self._db)

        return user

    def create_superuser(self, username, password=None):
        user = self.create_user(
            username=username,
            is_active=True,
            password=password,
        )

        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(BaseModel, AbstractBaseUser, PermissionsMixin):

    username = models.CharField(max_length=255, unique=True)

    email = models.EmailField(verbose_name = "email address",
                              unique=True)

    is_active = models.BooleanField(default=True)

    objects = BaseUserManager()

    USERNAME_FIELD = 'username'


    def __str__(self):
        return self.username

