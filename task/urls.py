from django.urls import path
from .views import TaskListView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'', TaskListView, basename='task')
urlpatterns = router.urls