from rest_framework.permissions import BasePermission
from authentication.models import Permission


class CanComment(BasePermission):
    message = 'You do not have comment permission.'

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        return request.user.has_app_permission(Permission.COMMENT)

    def has_object_permission(self, request, view, obj):
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        # Author can edit/delete their own comment
        if obj.author == request.user:
            return True
        # Moderators can delete/edit any comment
        return request.user.has_app_permission(Permission.MODERATE)
