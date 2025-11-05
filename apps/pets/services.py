"""
Pets app services.
Contains business logic for pet operations (write operations).
"""

from django.utils import timezone
from .models import Pet, SuccessStory
from apps.core.utils import generate_unique_slug


class PetService:
    """Service for Pet model operations"""
    
    @staticmethod
    def create_pet(*, name: str, type: str, breed: str, **kwargs) -> Pet:
        """
        Create a new pet.
        
        Args:
            name: Pet name
            type: Pet type (dog, cat, etc.)
            breed: Pet breed
            **kwargs: Additional pet fields
        
        Returns:
            Created Pet instance
        """
        slug = generate_unique_slug(Pet, name)
        
        pet = Pet.objects.create(
            name=name,
            slug=slug,
            type=type,
            breed=breed,
            **kwargs
        )
        
        return pet
    
    @staticmethod
    def update_pet(*, pet: Pet, **data) -> Pet:
        """
        Update a pet.
        
        Args:
            pet: Pet instance to update
            **data: Fields to update
        
        Returns:
            Updated Pet instance
        """
        for key, value in data.items():
            setattr(pet, key, value)
        
        pet.save()
        return pet
    
    @staticmethod
    def update_pet_status(*, pet: Pet, status: str) -> Pet:
        """
        Update pet status.
        
        Args:
            pet: Pet instance
            status: New status
        
        Returns:
            Updated Pet instance
        """
        pet.status = status
        pet.save()
        return pet
    
    @staticmethod
    def mark_pet_adopted(*, pet: Pet) -> Pet:
        """
        Mark a pet as adopted.
        
        Args:
            pet: Pet instance
        
        Returns:
            Updated Pet instance
        """
        return PetService.update_pet_status(pet=pet, status='adopted')
    
    @staticmethod
    def mark_pet_available(*, pet: Pet) -> Pet:
        """
        Mark a pet as available.
        
        Args:
            pet: Pet instance
        
        Returns:
            Updated Pet instance
        """
        return PetService.update_pet_status(pet=pet, status='available')


class SuccessStoryService:
    """Service for SuccessStory model operations"""
    
    @staticmethod
    def create_success_story(
        *,
        title: str,
        story: str,
        adopter_name: str,
        adoption_date,
        **kwargs
    ) -> SuccessStory:
        """
        Create a success story.
        
        Args:
            title: Story title
            story: Story content
            adopter_name: Name of adopter
            adoption_date: Date of adoption
            **kwargs: Additional fields
        
        Returns:
            Created SuccessStory instance
        """
        success_story = SuccessStory.objects.create(
            title=title,
            story=story,
            adopter_name=adopter_name,
            adoption_date=adoption_date,
            **kwargs
        )
        
        return success_story