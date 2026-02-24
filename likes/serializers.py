from rest_framework import serializers
from .models import Like


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ["id", "article", "user", "created_at"]
        read_only_fields = fields


class LikeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ["article"]

    def validate_article(self, value):
        user = self.context["request"].user
        if Like.objects.filter(article=value, user=user).exists():
            raise serializers.ValidationError("You have already liked this article.")
        return value
