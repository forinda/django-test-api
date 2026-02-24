from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes
from .models import Article
from category.serializers import CategorySerializer


class ArticleListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    author_email = serializers.EmailField(source='author.email', read_only=True)

    class Meta:
        model = Article
        fields = '__all__'


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'


class BinaryImageField(serializers.ImageField):
    pass


extend_schema_field(OpenApiTypes.BINARY)(BinaryImageField)


class ArticleCreateSerializer(serializers.ModelSerializer):
    cover_image = BinaryImageField(required=False, allow_null=True)

    class Meta:
        model = Article
        fields = [
            'title', 'slug', 'body', 'excerpt',
            'category', 'cover_image', 'status',
        ]


class ArticleUpdateSerializer(serializers.ModelSerializer):
    cover_image = BinaryImageField(required=False, allow_null=True)

    class Meta:
        model = Article
        fields = [
            'title', 'slug', 'body', 'excerpt',
            'category', 'cover_image', 'status',
        ]
