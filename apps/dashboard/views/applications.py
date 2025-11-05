"""
Dashboard app - application management views.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils import timezone

from apps.adoptions.models import AdoptionApplication
from apps.adoptions.selectors import filter_applications, get_application_by_id
from apps.adoptions.services import AdoptionApplicationService
from ..decorators import admin_required


@admin_required
def applications_list(request):
    """Admin view for managing all applications"""
    # Build filters
    filters = {}
    
    if status_filter := request.GET.get('status'):
        filters['status'] = status_filter
    
    if search_query := request.GET.get('search'):
        filters['search'] = search_query
    
    applications = filter_applications(filters=filters if filters else None)
    
    # Pagination
    paginator = Paginator(applications, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'applications': page_obj,
        'total_applications': applications.count(),
        'is_paginated': page_obj.has_other_pages(),
        'page_obj': page_obj,
    }
    return render(request, 'dashboard/admin_applications.html', context)


@admin_required
def application_detail(request, application_id):
    """Detailed view of a single application"""
    application = get_object_or_404(AdoptionApplication, id=application_id)
    
    context = {
        'application': application,
    }
    return render(request, 'dashboard/admin_application_detail.html', context)


@admin_required
def update_application_status(request, application_id):
    """Update application status"""
    if request.method == 'POST':
        application = get_application_by_id(application_id=application_id)
        new_status = request.POST.get('status')
        
        if new_status in ['pending', 'approved', 'rejected', 'completed']:
            AdoptionApplicationService.update_application_status(
                application=application,
                status=new_status
            )
            messages.success(
                request,
                f'Application status updated to {application.get_status_display()}'
            )
        else:
            messages.error(request, 'Invalid status')
    
    # Redirect back to the referring page or application detail
    next_url = request.META.get('HTTP_REFERER')
    if next_url and 'application_detail' in str(next_url):
        return redirect('dashboard:application_detail', application_id=application_id)
    else:
        return redirect('dashboard:applications')


@admin_required
def update_application_notes(request, application_id):
    """Update admin notes for an application"""
    if request.method == 'POST':
        application = get_application_by_id(application_id=application_id)
        notes = request.POST.get('notes', '')
        
        AdoptionApplicationService.update_application_notes(
            application=application,
            notes=notes
        )
        
        messages.success(request, 'Notes updated successfully')
    
    return redirect('dashboard:application_detail', application_id=application_id)