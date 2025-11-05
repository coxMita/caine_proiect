"""
Adoptions app views.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from apps.pets.models import Pet
from apps.pets.selectors import get_available_pets
from .services import AdoptionApplicationService
from .selectors import get_user_applications


def adoption_gate(request, pet_id=None):
    """
    If logged in -> jump straight to the adoption form.
    If logged out -> show a page with Login / Register options.
    """
    # Build where we want to land after auth
    if pet_id:
        next_url = reverse('adoptions:application_pet', args=[pet_id])
    else:
        next_url = reverse('adoptions:application')
    
    if request.user.is_authenticated:
        return redirect(next_url)
    
    return render(request, 'adoptions/adoption_gate.html', {'next': next_url})


def adoption_process(request):
    """Adoption process information page"""
    return render(request, 'adoptions/adoption.html')


@login_required(login_url='accounts:login')
def adoption_application(request, pet_id=None):
    """Adoption application form"""
    pet = None
    if pet_id:
        pet = get_object_or_404(Pet, pk=pet_id, status='available')
    
    if request.method == 'POST':
        # Get the pet
        if not pet:
            pet = get_object_or_404(Pet, pk=request.POST.get('pet_id'))
        
        # Create application using service
        application = AdoptionApplicationService.create_application(
            user=request.user,
            pet=pet,
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            address=request.POST.get('address'),
            housing_type=request.POST.get('housing_type'),
            own_or_rent=request.POST.get('own_or_rent'),
            landlord_approval=request.POST.get('landlord_approval') == 'yes',
            household_adults=int(request.POST.get('household_adults', 1)),
            household_children=int(request.POST.get('household_children', 0)),
            has_other_pets=request.POST.get('has_other_pets') == 'yes',
            other_pets_description=request.POST.get('other_pets_description', ''),
            previous_pet_experience=request.POST.get('previous_pet_experience'),
            reason_for_adoption=request.POST.get('reason_for_adoption'),
        )
        
        messages.success(
            request,
            'Your application has been submitted successfully! We will review it and contact you soon.'
        )
        
        return redirect('accounts:applications')
    
    context = {
        'pet': pet,
        'available_pets': get_available_pets() if not pet else None
    }
    return render(request, 'adoptions/adoption_application.html', context)


@login_required
def user_applications(request):
    """View all user's adoption applications"""
    applications = get_user_applications(user=request.user)
    
    context = {
        'applications': applications,
    }
    return render(request, 'accounts/user_applications.html', context)