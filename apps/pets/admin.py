"""
Pets app admin.
"""

from django.contrib import admin
from .models import Pet, SuccessStory


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'breed', 'age', 'gender', 'status', 'featured', 'arrival_date')
    list_filter = ('type', 'size', 'gender', 'status', 'featured', 'special_needs')
    search_fields = ('name', 'breed', 'description')
    prepopulated_fields = {'slug': ('name',)}
    date_hierarchy = 'arrival_date'
    ordering = ('-arrival_date',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'type', 'breed', 'age', 'gender', 'size', 'color')
        }),
        ('Description', {
            'fields': ('description', 'personality')
        }),
        ('Medical Information', {
            'fields': ('vaccinated', 'spayed_neutered', 'microchipped', 
                      'special_needs', 'special_needs_description')
        }),
        ('Images', {
            'fields': ('main_image', 'image_2', 'image_3')
        }),
        ('Status & Fees', {
            'fields': ('status', 'arrival_date', 'adoption_fee', 'featured')
        }),
    )


@admin.register(SuccessStory)
class SuccessStoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'adopter_name', 'pet', 'adoption_date', 'featured')
    list_filter = ('featured', 'adoption_date')
    search_fields = ('title', 'adopter_name', 'story')
    date_hierarchy = 'adoption_date'
    ordering = ('-adoption_date',)