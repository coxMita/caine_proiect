"""
Adoptions app services.
Contains business logic for adoption operations (write operations).
"""

from django.utils import timezone
from .models import AdoptionApplication


class AdoptionApplicationService:
    """Service for AdoptionApplication operations"""
    
    @staticmethod
    def create_application(
        *,
        pet,
        first_name: str,
        last_name: str,
        email: str,
        phone: str,
        address: str,
        housing_type: str,
        own_or_rent: str,
        household_adults: int,
        previous_pet_experience: str,
        reason_for_adoption: str,
        user=None,
        **kwargs
    ) -> AdoptionApplication:
        """
        Create a new adoption application.
        
        Args:
            pet: Pet instance
            first_name: Applicant first name
            last_name: Applicant last name
            email: Applicant email
            phone: Applicant phone
            address: Applicant address
            housing_type: Type of housing
            own_or_rent: Own or rent
            household_adults: Number of adults
            previous_pet_experience: Previous pet experience text
            reason_for_adoption: Reason for adoption text
            user: Optional User instance (if logged in)
            **kwargs: Additional fields
        
        Returns:
            Created AdoptionApplication instance
        """
        application = AdoptionApplication.objects.create(
            user=user,
            pet=pet,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            address=address,
            housing_type=housing_type,
            own_or_rent=own_or_rent,
            household_adults=household_adults,
            previous_pet_experience=previous_pet_experience,
            reason_for_adoption=reason_for_adoption,
            **kwargs
        )
        
        return application
    
    @staticmethod
    def update_application_status(
        *,
        application: AdoptionApplication,
        status: str
    ) -> AdoptionApplication:
        """
        Update application status.
        
        Args:
            application: AdoptionApplication instance
            status: New status
        
        Returns:
            Updated AdoptionApplication instance
        """
        old_status = application.status
        application.status = status
        application.reviewed_at = timezone.now()
        application.save()
        
        # Update pet status if application is completed
        if status == 'completed':
            from apps.pets.services import PetService
            PetService.mark_pet_adopted(pet=application.pet)
        elif old_status == 'completed' and status != 'completed':
            # If changing from completed to something else, make pet available again
            from apps.pets.services import PetService
            PetService.mark_pet_available(pet=application.pet)
        
        return application
    
    @staticmethod
    def update_application_notes(
        *,
        application: AdoptionApplication,
        notes: str
    ) -> AdoptionApplication:
        """
        Update admin notes for an application.
        
        Args:
            application: AdoptionApplication instance
            notes: Admin notes
        
        Returns:
            Updated AdoptionApplication instance
        """
        application.notes = notes
        application.reviewed_at = timezone.now()
        application.save()
        
        return application