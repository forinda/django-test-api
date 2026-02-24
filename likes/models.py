from django.db import models
from django.conf import settings
from mixins.model_mixin import AuditModel


class Like(AuditModel):
    article = models.ForeignKey(
        'articles.Article',
        on_delete=models.CASCADE,
        related_name='likes',
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='likes',
    )

    class Meta:
        unique_together = ('article', 'user')
        ordering = ['-created_at']
        verbose_name_plural = 'Likes'

    def __str__(self):
        return f'Like by {self.user_id} on {self.article_id}'
