"""
Dashboard app - main dashboard view.
"""

from django.shortcuts import render

from apps.adoptions.selectors import get_recent_applications
from apps.contact.selectors import get_recent_messages
from ..decorators import admin_required
from ..services import DashboardStatsService


@admin_required
def dashboard_home(request):
    """Admin dashboard with overview statistics"""
    stats = DashboardStatsService.get_dashboard_stats()
    recent_applications = get_recent_applications(limit=5)
    recent_contacts = get_recent_messages(limit=5)
    
    context = {
        'stats': stats,
        'recent_applications': recent_applications,
        'recent_contacts': recent_contacts,
    }
    return render(request, 'dashboard/admin_dashboard.html', context)