from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .seriallizers import TaskSerializer, TaskCreateSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework.parsers import MultiPartParser, FormParser,FileUploadParser
from .models import Task


# Create your views here.
@extend_schema(tags=['Task'], request=TaskCreateSerializer, responses=TaskSerializer)
class TaskListView(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    parser_classes = (MultiPartParser, FormParser, FileUploadParser)

    # def list(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)
