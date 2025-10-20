from rest_framework.permissions import BasePermission

from apps.models import User


class  IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        if request.user.role == User.RoleType.ADMIN:
            return True
        else:
            return False
