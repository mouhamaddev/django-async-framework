from datetime import timedelta
from django.utils import timezone
from django.db import models

class EntityQuerySet(models.QuerySet):
    def recent(self):
        recent_time = timezone.now() - timedelta(days=1)
        return self.filter(created_at__gte=recent_time)

class EntityManager(models.Manager):
    def get_queryset(self):
        return EntityQuerySet(self.model, using=self._db)

class Entity(models.Model):
    objects = EntityManager()

    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description
