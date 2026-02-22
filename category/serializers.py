from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CategoryWithTasksSerializer(serializers.ModelSerializer):
    tasks = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = '__all__'

    def get_tasks(self, obj):
        from task.seriallizers import TaskSerializer
        return TaskSerializer(obj.tasks.all(), many=True).data