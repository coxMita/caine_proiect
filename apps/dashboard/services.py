"""
Dashboard app services.
Contains business logic for dashboard operations.
"""

from apps.pets.models import Pet
from apps.adoptions.models import AdoptionApplication
from apps.contact.models import ContactMessage


class DashboardStatsService:
    """Service for dashboard statistics"""
    
    @staticmethod
    def get_dashboard_stats() -> dict:
        """
        Get dashboard statistics.
        
        Returns:
            Dict with dashboard stats
        """
        return {
            'pending_applications': AdoptionApplication.objects.filter(status='pending').count(),
            'available_pets': Pet.objects.filter(status='available').count(),
            'total_adopted': Pet.objects.filter(status='adopted').count(),
            'unread_messages': ContactMessage.objects.filter(is_read=False).count(),
        }