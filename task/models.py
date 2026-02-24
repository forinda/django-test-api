from django.db import models
from django.utils import timezone
from mixins.model_mixin import AuditModel


# Create your models here.
class Task(AuditModel):
    class Priority(models.TextChoices):
        LOW = "Low", "Low"
        MEDIUM = "Medium", "Medium"
        HIGH = "High", "High"

    title = models.CharField(max_length=200)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    category = models.ForeignKey(
        "category.Category", on_delete=models.CASCADE, related_name="tasks", null=True
    )
    thumbnail = models.ImageField(upload_to="thumbnails/", null=True, blank=True)
    priority = models.CharField(
        max_length=10, choices=Priority.choices, default=Priority.LOW
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Tasks"

    def __str__(self):
        return self.title
