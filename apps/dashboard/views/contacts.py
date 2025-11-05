"""
Dashboard app - contact message management views.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator

from apps.contact.models import ContactMessage
from apps.contact.selectors import filter_contact_messages, get_contact_message_by_id
from apps.contact.services import ContactMessageService
from ..decorators import admin_required


@admin_required
def contacts_list(request):
    """Admin view for managing contact messages"""
    # Build filters
    filters = {}
    
    if read_filter := request.GET.get('read'):
        filters['read'] = read_filter
    
    if search_query := request.GET.get('search'):
        filters['search'] = search_query
    
    contacts = filter_contact_messages(filters=filters if filters else None)
    
    # Pagination
    paginator = Paginator(contacts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'contacts': page_obj,
        'total_contacts': contacts.count(),
        'is_paginated': page_obj.has_other_pages(),
        'page_obj': page_obj,
    }
    return render(request, 'dashboard/admin_contacts.html', context)


@admin_required
def contact_detail(request, contact_id):
    """Detailed view of a contact message"""
    contact = get_object_or_404(ContactMessage, id=contact_id)
    
    # Mark as read if not already
    if not contact.is_read:
        ContactMessageService.mark_as_read(message=contact)
    
    context = {
        'contact': contact,
    }
    return render(request, 'dashboard/admin_contact_detail.html', context)


@admin_required
def update_contact_status(request, contact_id):
    """Update contact message status"""
    if request.method == 'POST':
        contact = get_contact_message_by_id(message_id=contact_id)
        action = request.POST.get('action')
        
        if action == 'mark_responded':
            ContactMessageService.mark_as_responded(message=contact)
            messages.success(request, 'Message marked as responded')
        elif action == 'mark_unresponded':
            ContactMessageService.update_message_status(
                message=contact,
                is_responded=False
            )
            messages.success(request, 'Message marked as not responded')
    
    return redirect('dashboard:contact_detail', contact_id=contact_id)