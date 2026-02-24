from rest_framework import serializers
from .models import Comment


class ReplySerializer(serializers.ModelSerializer):
    author_email = serializers.EmailField(source='author.email', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'author_email', 'body', 'created_at', 'updated_at']
        read_only_fields = fields


class CommentListSerializer(serializers.ModelSerializer):
    author_email = serializers.EmailField(source='author.email', read_only=True)
    replies = ReplySerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id', 'article', 'author', 'author_email',
            'body', 'parent', 'replies', 'created_at', 'updated_at',
        ]
        read_only_fields = fields


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['article', 'body', 'parent']


class CommentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['body']
