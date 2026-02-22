from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class BinaryImageField(serializers.ImageField):
    pass


extend_schema_field(OpenApiTypes.BINARY)(BinaryImageField)


class TaskCreateSerializer(serializers.ModelSerializer):
    thumbnail = BinaryImageField(required=False, allow_null=True)

    class Meta:
        model = Task
        fields = '__all__'
