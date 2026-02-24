from django.db import models
from mixins.model_mixin import AuditModel


# Create your models here.
class Category(AuditModel):
    name = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
