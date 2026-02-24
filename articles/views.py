from django.db.models import Count, Exists, OuterRef
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema

from .models import Article
from likes.models import Like
from comments.models import Comment
from .serializers import (
    ArticleSerializer,
    ArticleListSerializer,
    ArticleCreateSerializer,
    ArticleUpdateSerializer,
)
from .permissions import CanWriteArticle


@extend_schema(tags=["Articles"])
class ArticleViewSet(ModelViewSet):
    serializer_class = ArticleListSerializer
    permission_classes = [IsAuthenticated, CanWriteArticle]
    parser_classes = (MultiPartParser, FormParser)
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["status", "category", "author"]
    search_fields = ["title", "body", "excerpt", "slug"]
    ordering_fields = ["created_at", "updated_at", "title"]
    ordering = ["-created_at"]

    def get_queryset(self):
        qs = Article.objects.select_related("category", "author").annotate(
            likes_count=Count("likes", distinct=True),
            comments_count=Count("comments", distinct=True),
            is_liked=Exists(
                Like.objects.filter(article=OuterRef("pk"), user=self.request.user)
            ),
        )
        return qs

    def get_serializer_class(self):
        if self.action == "create":
            return ArticleCreateSerializer
        if self.action in ["update", "partial_update"]:
            return ArticleUpdateSerializer
        return ArticleListSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @extend_schema(
        tags=["Articles"],
        request={"multipart/form-data": ArticleCreateSerializer},
        responses=ArticleSerializer,
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        tags=["Articles"],
        request={"multipart/form-data": ArticleUpdateSerializer},
        responses=ArticleSerializer,
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        tags=["Articles"],
        request={"multipart/form-data": ArticleUpdateSerializer},
        responses=ArticleSerializer,
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
