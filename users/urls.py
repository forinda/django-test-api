from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, RoleViewSet

user_router = DefaultRouter()
user_router.register(r"", UserViewSet, basename="user")

role_router = DefaultRouter()
role_router.register(r"", RoleViewSet, basename="role")

urlpatterns = [
    path("roles/", include(role_router.urls)),
    path("", include(user_router.urls)),
]
