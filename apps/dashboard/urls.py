"""
Dashboard app URLs.
"""

from django.urls import path
from .views import (
    dashboard_home,
    applications_list,
    application_detail,
    update_application_status,
    update_application_notes,
    pets_list,
    contacts_list,
    contact_detail,
    update_contact_status,
)

app_name = 'dashboard'

urlpatterns = [
    # Main dashboard
    path('', dashboard_home, name='home'),
    
    # Applications management
    path('applications/', applications_list, name='applications'),
    path('applications/<int:application_id>/', application_detail, name='application_detail'),
    path('applications/<int:application_id>/update-status/', update_application_status, name='update_application_status'),
    path('applications/<int:application_id>/update-notes/', update_application_notes, name='update_application_notes'),
    
    # Pets management
    path('pets/', pets_list, name='pets'),
    
    # Contacts management
    path('contacts/', contacts_list, name='contacts'),
    path('contacts/<int:contact_id>/', contact_detail, name='contact_detail'),
    path('contacts/<int:contact_id>/update-status/', update_contact_status, name='update_contact_status'),
]