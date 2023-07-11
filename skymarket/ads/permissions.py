from rest_framework.permissions import BasePermission

from users.models import UserRoles


class IsOwner(BasePermission):
    message = "This action is only allowed to the owner."
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsAdmin(BasePermission):
    message = "This action is allowed only to the admin."
    def has_permission(self, request, view):
        return request.user.role == UserRoles.ADMIN
