from rest_framework.routers import DefaultRouter
from .views import UserViewSet, RoleViewSet

router = DefaultRouter()
router.register(r'', UserViewSet, basename='user')
router.register(r'roles', RoleViewSet, basename='role')
urlpatterns = router.urls
