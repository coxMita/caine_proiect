"""
Pets app selectors.
Contains query logic for retrieving pet data (read operations only).
"""

from django.db.models import Q, QuerySet
from .models import Pet, SuccessStory


def get_available_pets(*, filters=None) -> QuerySet:
    """
    Get all available pets with optional filters.
    
    Args:
        filters: Dict of filter parameters
    
    Returns:
        QuerySet of available pets
    """
    queryset = Pet.objects.filter(status='available')
    
    if filters:
        # Filter by type
        if filters.get('type') and filters['type'] != 'all':
            queryset = queryset.filter(type=filters['type'])
        
        # Filter by size
        if filters.get('sizes'):
            queryset = queryset.filter(size__in=filters['sizes'])
        
        # Filter by special needs
        if filters.get('special_needs'):
            queryset = queryset.filter(special_needs=True)
        
        # Search by name or breed
        if filters.get('search'):
            queryset = queryset.filter(
                Q(name__icontains=filters['search']) |
                Q(breed__icontains=filters['search']) |
                Q(description__icontains=filters['search'])
            )
    
    return queryset


def get_featured_pets(*, limit=3) -> QuerySet:
    """
    Get featured pets that are available.
    
    Args:
        limit: Maximum number of pets to return
    
    Returns:
        QuerySet of featured pets
    """
    return Pet.objects.filter(featured=True, status='available')[:limit]


def get_pet_by_id(*, pet_id: int) -> Pet:
    """
    Get a pet by ID.
    
    Args:
        pet_id: Pet ID
    
    Returns:
        Pet instance
    """
    return Pet.objects.get(pk=pet_id)


def get_related_pets(*, pet: Pet, limit=3) -> QuerySet:
    """
    Get related pets (same type, different pet).
    
    Args:
        pet: Pet instance to find related pets for
        limit: Maximum number of related pets to return
    
    Returns:
        QuerySet of related pets
    """
    return Pet.objects.filter(
        type=pet.type,
        status='available'
    ).exclude(pk=pet.pk)[:limit]


def get_success_stories(*, featured_only=False) -> QuerySet:
    """
    Get success stories.
    
    Args:
        featured_only: If True, only return featured stories
    
    Returns:
        QuerySet of success stories
    """
    queryset = SuccessStory.objects.all()
    
    if featured_only:
        queryset = queryset.filter(featured=True)
    
    return queryset


def get_pet_stats() -> dict:
    """
    Get statistics about pets.
    
    Returns:
        Dict with pet statistics
    """
    from apps.adoptions.models import AdoptionApplication
    
    return {
        'total_adopted': Pet.objects.filter(status='adopted').count(),
        'available_now': Pet.objects.filter(status='available').count(),
        'happy_families': AdoptionApplication.objects.filter(status='completed').count(),
        'years_of_service': 8,
    }