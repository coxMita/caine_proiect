"""
Dashboard app - pet management views.
"""

from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator

from apps.pets.models import Pet
from ..decorators import admin_required


@admin_required
def pets_list(request):
    """Admin view for managing pets"""
    pets = Pet.objects.all().prefetch_related('applications').order_by('-arrival_date')
    
    # Filter by status
    if status_filter := request.GET.get('status'):
        pets = pets.filter(status=status_filter)
    
    # Filter by type
    if type_filter := request.GET.get('type'):
        pets = pets.filter(type=type_filter)
    
    # Search
    if search_query := request.GET.get('search'):
        pets = pets.filter(
            Q(name__icontains=search_query) |
            Q(breed__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(pets, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'pets': page_obj,
        'total_pets': pets.count(),
        'is_paginated': page_obj.has_other_pages(),
        'page_obj': page_obj,
    }
    return render(request, 'dashboard/admin_pets.html', context)