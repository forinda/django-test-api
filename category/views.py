from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import CategorySerializer
from .models import Category
from drf_spectacular.utils import extend_schema

# Create your views here.
@extend_schema(tags=['Category'])
class CategoryListView(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer