from rest_framework.permissions import BasePermission
from authentication.models import Permission


class CanWriteArticle(BasePermission):
    message = 'You do not have write permission for articles.'

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        return request.user.has_app_permission(Permission.WRITE)
