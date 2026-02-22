from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import CategorySerializer, CategoryWithTasksSerializer
from .models import Category
from drf_spectacular.utils import extend_schema


# Create your views here.
@extend_schema(tags=['Category'])
class CategoryListView(ModelViewSet):
    queryset = Category.objects.prefetch_related('tasks').all()
    serializer_class = CategoryWithTasksSerializer

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CategorySerializer
        return CategoryWithTasksSerializer