"""
Adoptions app admin.
"""

from django.contrib import admin
from .models import AdoptionApplication


@admin.register(AdoptionApplication)
class AdoptionApplicationAdmin(admin.ModelAdmin):
    list_display = ('applicant_name', 'pet', 'email', 'phone', 'status', 'submitted_at')
    list_filter = ('status', 'submitted_at', 'housing_type', 'has_other_pets')
    search_fields = ('first_name', 'last_name', 'email', 'pet__name')
    date_hierarchy = 'submitted_at'
    ordering = ('-submitted_at',)
    readonly_fields = ('submitted_at',)
    
    def applicant_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    applicant_name.short_description = 'Applicant'
    
    fieldsets = (
        ('Applicant Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'address')
        }),
        ('Pet Selection', {
            'fields': ('pet',)
        }),
        ('Housing Information', {
            'fields': ('housing_type', 'own_or_rent', 'landlord_approval')
        }),
        ('Household Information', {
            'fields': ('household_adults', 'household_children', 
                      'has_other_pets', 'other_pets_description')
        }),
        ('Experience & Reason', {
            'fields': ('previous_pet_experience', 'reason_for_adoption')
        }),
        ('Application Status', {
            'fields': ('status', 'submitted_at', 'reviewed_at', 'notes')
        }),
    )