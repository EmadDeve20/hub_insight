from rest_framework.permissions import BasePermission

class CreateUserPermission(BasePermission):

    def has_permission(self, request, view):
        # user permission to create user from default django permissions:
        # return request.user.has_perm("user.add_user")
        
        # For just superusers:
        
        return request.user.is_superuser

