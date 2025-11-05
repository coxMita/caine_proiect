"""
Adoptions app models.
"""

from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel


class AdoptionApplication(TimeStampedModel):
    """Model for adoption applications"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Adoption Completed'),
    ]
    
    # User Link (optional - for logged-in users)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='applications'
    )
    
    # Applicant Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    
    # Pet Selection
    pet = models.ForeignKey(
        'pets.Pet',
        on_delete=models.CASCADE,
        related_name='applications'
    )
    
    # Housing Information
    housing_type = models.CharField(max_length=50)
    own_or_rent = models.CharField(max_length=20)
    landlord_approval = models.BooleanField(default=False)
    
    # Household Information
    household_adults = models.IntegerField()
    household_children = models.IntegerField(default=0)
    has_other_pets = models.BooleanField(default=False)
    other_pets_description = models.TextField(blank=True)
    
    # Experience and Commitment
    previous_pet_experience = models.TextField()
    reason_for_adoption = models.TextField()
    
    # Application Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-submitted_at']
        verbose_name = 'Adoption Application'
        verbose_name_plural = 'Adoption Applications'
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.pet.name}"