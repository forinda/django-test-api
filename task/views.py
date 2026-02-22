from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .seriallizers import TaskSerializer, TaskCreateSerializer,TaskListSerializer
from drf_spectacular.utils import extend_schema
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Task


# Create your views here.
class TaskListView(ModelViewSet):
    queryset = Task.objects.select_related('category').all()
    serializer_class = TaskSerializer
    parser_classes = (MultiPartParser, FormParser)

    @extend_schema(tags=['Task'], responses=TaskListSerializer)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(tags=['Task'], responses=TaskListSerializer)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        tags=['Task'],
        request={'multipart/form-data': TaskCreateSerializer},
        responses=TaskSerializer,
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        tags=['Task'],
        request={'multipart/form-data': TaskCreateSerializer},
        responses=TaskSerializer,
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        tags=['Task'],
        request={'multipart/form-data': TaskCreateSerializer},
        responses=TaskSerializer,
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(tags=['Task'])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return TaskCreateSerializer
        return TaskListSerializer
