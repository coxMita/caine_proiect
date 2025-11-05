"""
Core utilities module.
Contains utility functions used across the application.
"""

from django.utils.text import slugify as django_slugify


def generate_unique_slug(model_class, title, slug_field='slug'):
    """
    Generate a unique slug for a model instance.
    
    Args:
        model_class: The model class
        title: The title to slugify
        slug_field: The name of the slug field (default: 'slug')
    
    Returns:
        A unique slug string
    """
    slug = django_slugify(title)
    unique_slug = slug
    num = 1
    
    while model_class.objects.filter(**{slug_field: unique_slug}).exists():
        unique_slug = f'{slug}-{num}'
        num += 1
    
    return unique_slug


def is_admin_user(user):
    """
    Check if user is staff/admin.
    
    Args:
        user: Django User instance
    
    Returns:
        Boolean indicating if user is admin
    """
    return user.is_authenticated and (user.is_staff or user.is_superuser)