from rest_framework.routers import DefaultRouter
from .views import CategoryListView

router = DefaultRouter()
router.register(r'', CategoryListView, basename='category')
urlpatterns = router.urls