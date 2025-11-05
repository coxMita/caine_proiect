"""
Adoptions app selectors.
Contains query logic for adoption applications (read operations only).
"""

from django.db.models import Q, QuerySet
from .models import AdoptionApplication


def get_user_applications(*, user) -> QuerySet:
    """
    Get all applications for a user (by user or email).
    
    Args:
        user: Django User instance
    
    Returns:
        QuerySet of applications
    """
    return AdoptionApplication.objects.filter(
        Q(user=user) | Q(email=user.email)
    ).order_by('-submitted_at')


def get_pending_applications() -> QuerySet:
    """
    Get all pending applications.
    
    Returns:
        QuerySet of pending applications
    """
    return AdoptionApplication.objects.filter(status='pending')


def get_application_by_id(*, application_id: int) -> AdoptionApplication:
    """
    Get an application by ID.
    
    Args:
        application_id: Application ID
    
    Returns:
        AdoptionApplication instance
    """
    return AdoptionApplication.objects.get(pk=application_id)


def get_recent_applications(*, limit=5) -> QuerySet:
    """
    Get recent applications.
    
    Args:
        limit: Maximum number of applications to return
    
    Returns:
        QuerySet of recent applications
    """
    return AdoptionApplication.objects.select_related('pet').order_by('-submitted_at')[:limit]


def filter_applications(*, filters=None) -> QuerySet:
    """
    Filter applications based on provided criteria.
    
    Args:
        filters: Dict of filter parameters
    
    Returns:
        QuerySet of filtered applications
    """
    queryset = AdoptionApplication.objects.select_related('pet').order_by('-submitted_at')
    
    if filters:
        # Filter by status
        if status := filters.get('status'):
            queryset = queryset.filter(status=status)
        
        # Search by applicant name, email, or pet name
        if search := filters.get('search'):
            queryset = queryset.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search) |
                Q(pet__name__icontains=search) |
                Q(pet__breed__icontains=search)
            )
    
    return queryset