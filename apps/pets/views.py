"""
Pets app views.
"""

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.db.models import Q

from .models import Pet
from .selectors import (
    get_available_pets,
    get_featured_pets,
    get_pet_by_id,
    get_related_pets,
    get_success_stories,
    get_pet_stats
)


def home(request):
    """Homepage view with featured pets and stats"""
    featured_pets = get_featured_pets(limit=3)
    stats = get_pet_stats()
    
    # Use fallback values if counts are zero
    if stats['total_adopted'] == 0:
        stats['total_adopted'] = 1247
    if stats['available_now'] == 0:
        stats['available_now'] = 15
    if stats['happy_families'] == 0:
        stats['happy_families'] = 156
    
    context = {
        'featured_pets': featured_pets,
        'stats': stats
    }
    return render(request, 'pets/index.html', context)


class PetListView(ListView):
    """View for browsing all pets with filters"""
    model = Pet
    template_name = 'pets/pets.html'
    context_object_name = 'pets'
    paginate_by = 9
    
    def get_queryset(self):
        # Build filters from GET parameters
        filters = {}
        
        if search := self.request.GET.get('search'):
            filters['search'] = search
        
        if pet_type := self.request.GET.get('type'):
            filters['type'] = pet_type
        
        if sizes := self.request.GET.getlist('size'):
            filters['sizes'] = sizes
        
        if self.request.GET.get('specialNeeds'):
            filters['special_needs'] = True
        
        queryset = get_available_pets(filters=filters if filters else None)
        
        # Apply sorting
        sort_by = self.request.GET.get('sort', 'newest')
        if sort_by == 'newest':
            queryset = queryset.order_by('-arrival_date')
        elif sort_by == 'oldest':
            queryset = queryset.order_by('arrival_date')
        elif sort_by == 'name':
            queryset = queryset.order_by('name')
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_pets'] = self.get_queryset().count()
        return context


class PetDetailView(DetailView):
    """View for individual pet detail page"""
    model = Pet
    template_name = 'pets/pet_detail.html'
    context_object_name = 'pet'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_pets'] = get_related_pets(pet=self.object, limit=3)
        return context


def about(request):
    """About page view"""
    return render(request, 'pets/about.html')


def success_stories(request):
    """Success stories page"""
    stories = get_success_stories()
    featured_stories = get_success_stories(featured_only=True)[:3]
    
    context = {
        'stories': stories,
        'featured_stories': featured_stories,
    }
    return render(request, 'pets/success.html', context)