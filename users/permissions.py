from rest_framework.permissions import BasePermission
from authentication.models import Permission


class IsAdmin(BasePermission):
    message = "You do not have admin privileges."

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.has_app_permission(Permission.ADMIN)
