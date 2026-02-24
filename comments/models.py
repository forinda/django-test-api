from django.db import models
from django.conf import settings
from mixins.model_mixin import AuditModel


class Comment(AuditModel):
    article = models.ForeignKey(
        'articles.Article',
        on_delete=models.CASCADE,
        related_name='comments',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    body = models.TextField()
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies',
    )

    class Meta:
        ordering = ['created_at']
        verbose_name_plural = 'Comments'

    def __str__(self):
        return f'Comment by {self.author_id} on {self.article_id}'
