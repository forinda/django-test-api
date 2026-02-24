from django.db import models
from django.conf import settings
from mixins.model_mixin import AuditModel


class Article(AuditModel):
    class Status(models.TextChoices):
        DRAFT = 'Draft', 'Draft'
        PUBLISHED = 'Published', 'Published'
        ARCHIVED = 'Archived', 'Archived'

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    body = models.TextField()
    excerpt = models.TextField(blank=True, default='')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='articles',
    )
    category = models.ForeignKey(
        'category.Category',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='articles',
    )
    cover_image = models.ImageField(upload_to='articles/', null=True, blank=True)
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.DRAFT,
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Articles'

    def __str__(self):
        return self.title
