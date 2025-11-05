"""
Core models module.
Contains abstract base models used across the application.
"""

from django.db import models


class TimeStampedModel(models.Model):
    """
    Abstract base model that provides timestamp fields.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class PublishableModel(TimeStampedModel):
    """
    Abstract base model for publishable content.
    """
    is_published = models.BooleanField(default=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        abstract = True