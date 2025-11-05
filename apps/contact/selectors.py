"""
Contact app selectors.
Contains query logic for contact messages (read operations only).
"""

from django.db.models import Q, QuerySet
from .models import ContactMessage


def get_contact_message_by_id(*, message_id: int) -> ContactMessage:
    """
    Get a contact message by ID.
    
    Args:
        message_id: Message ID
    
    Returns:
        ContactMessage instance
    """
    return ContactMessage.objects.get(pk=message_id)


def get_unread_messages() -> QuerySet:
    """
    Get all unread contact messages.
    
    Returns:
        QuerySet of unread messages
    """
    return ContactMessage.objects.filter(is_read=False)


def get_recent_messages(*, limit=5) -> QuerySet:
    """
    Get recent contact messages.
    
    Args:
        limit: Maximum number of messages to return
    
    Returns:
        QuerySet of recent messages
    """
    return ContactMessage.objects.order_by('-created_at')[:limit]


def filter_contact_messages(*, filters=None) -> QuerySet:
    """
    Filter contact messages based on provided criteria.
    
    Args:
        filters: Dict of filter parameters
    
    Returns:
        QuerySet of filtered messages
    """
    queryset = ContactMessage.objects.all().order_by('-created_at')
    
    if filters:
        # Filter by read status
        if read_filter := filters.get('read'):
            if read_filter == 'unread':
                queryset = queryset.filter(is_read=False)
            elif read_filter == 'read':
                queryset = queryset.filter(is_read=True)
        
        # Search by name, email, or subject
        if search := filters.get('search'):
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(email__icontains=search) |
                Q(subject__icontains=search)
            )
    
    return queryset