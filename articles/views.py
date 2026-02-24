from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from drf_spectacular.utils import extend_schema

from .models import Article
from .serializers import (
    ArticleSerializer,
    ArticleListSerializer,
    ArticleCreateSerializer,
    ArticleUpdateSerializer,
)
from .permissions import CanWriteArticle


@extend_schema(tags=['Articles'])
class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.select_related('category', 'author').all()
    serializer_class = ArticleListSerializer
    permission_classes = [IsAuthenticated, CanWriteArticle]
    parser_classes = (MultiPartParser, FormParser)

    def get_serializer_class(self):
        if self.action == 'create':
            return ArticleCreateSerializer
        if self.action in ['update', 'partial_update']:
            return ArticleUpdateSerializer
        return ArticleListSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @extend_schema(
        tags=['Articles'],
        request={'multipart/form-data': ArticleCreateSerializer},
        responses=ArticleSerializer,
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        tags=['Articles'],
        request={'multipart/form-data': ArticleUpdateSerializer},
        responses=ArticleSerializer,
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        tags=['Articles'],
        request={'multipart/form-data': ArticleUpdateSerializer},
        responses=ArticleSerializer,
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
