from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

class TaskCreateSerializer(serializers.ModelSerializer):
    thumbnail = serializers.ImageField(required=False)
    class Meta:
        model = Task
        fields = '__all__'