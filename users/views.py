from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from authentication.models import User, Role
from .serializers import (
    UserListSerializer,
    UserCreateSerializer,
    UserUpdateSerializer,
    RoleListSerializer,
)
from .permissions import IsAdmin


@extend_schema(tags=["Users"])
class UserViewSet(ModelViewSet):
    queryset = User.objects.select_related("role").all()
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer
        if self.action in ["update", "partial_update"]:
            return UserUpdateSerializer
        return UserListSerializer


@extend_schema(tags=["Roles"])
class RoleViewSet(ReadOnlyModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleListSerializer
    permission_classes = [IsAuthenticated]
