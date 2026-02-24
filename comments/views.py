from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from .models import Comment
from .serializers import CommentListSerializer, CommentCreateSerializer, CommentUpdateSerializer
from .permissions import CanComment


@extend_schema(tags=['Comments'])
class CommentViewSet(ModelViewSet):
    serializer_class = CommentListSerializer
    permission_classes = [IsAuthenticated, CanComment]

    def get_queryset(self):
        qs = Comment.objects.select_related('author', 'article').prefetch_related('replies__author')
        article_id = self.request.query_params.get('article')
        if article_id:
            qs = qs.filter(article_id=article_id)
        # Only return top-level comments for list; replies are nested
        if self.action == 'list':
            qs = qs.filter(parent=None)
        return qs

    def get_serializer_class(self):
        if self.action == 'create':
            return CommentCreateSerializer
        if self.action in ['update', 'partial_update']:
            return CommentUpdateSerializer
        return CommentListSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
