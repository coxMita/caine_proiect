"""
Adoptions app forms.
"""

from django import forms
from django.core.exceptions import ValidationError
from .models import AdoptionApplication
from apps.pets.models import Pet


class AdoptionApplicationForm(forms.ModelForm):
    """
    Form for adoption applications.
    
    This form handles all adoption application data with proper validation
    and widget customization for a better user experience.
    """
    
    # Override field to make it required with custom widget
    landlord_approval = forms.BooleanField(
        required=False,
        label="Do you have landlord approval for pets?",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    class Meta:
        model = AdoptionApplication
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone',
            'address',
            'pet',
            'housing_type',
            'own_or_rent',
            'landlord_approval',
            'household_adults',
            'household_children',
            'has_other_pets',
            'other_pets_description',
            'previous_pet_experience',
            'reason_for_adoption',
        ]
        
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your first name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your last name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your.email@example.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(555) 123-4567'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter your complete address including city, state, and ZIP'
            }),
            'pet': forms.Select(attrs={
                'class': 'form-control'
            }),
            'housing_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'own_or_rent': forms.Select(attrs={
                'class': 'form-control'
            }),
            'household_adults': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'value': 1
            }),
            'household_children': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'value': 0
            }),
            'has_other_pets': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'other_pets_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Please describe your other pets (type, breed, age, temperament)'
            }),
            'previous_pet_experience': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Tell us about your previous experience with pets...'
            }),
            'reason_for_adoption': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Why do you want to adopt this pet? What can you offer them?'
            }),
        }
        
        labels = {
            'first_name': 'First Name *',
            'last_name': 'Last Name *',
            'email': 'Email Address *',
            'phone': 'Phone Number *',
            'address': 'Full Address *',
            'pet': 'Select Pet *',
            'housing_type': 'Type of Housing *',
            'own_or_rent': 'Do you own or rent? *',
            'household_adults': 'Number of Adults in Household *',
            'household_children': 'Number of Children in Household',
            'has_other_pets': 'Do you have other pets?',
            'other_pets_description': 'Please describe your other pets',
            'previous_pet_experience': 'Previous Pet Experience *',
            'reason_for_adoption': 'Why do you want to adopt this pet? *',
        }
        
        help_texts = {
            'email': 'We will use this email to contact you about your application',
            'phone': 'Please provide a phone number where we can reach you',
            'address': 'Include street, city, state, and ZIP code',
            'household_adults': 'Total number of adults (18+) living in your home',
            'household_children': 'Total number of children under 18',
            'previous_pet_experience': 'Tell us about any pets you have owned before',
        }
    
    def __init__(self, *args, **kwargs):
        """
        Initialize form with custom logic.
        
        Can accept 'pet' parameter to pre-select a specific pet.
        """
        pet = kwargs.pop('pet', None)
        super().__init__(*args, **kwargs)
        
        # If specific pet is provided, set it as initial value and hide the field
        if pet:
            self.fields['pet'].initial = pet
            self.fields['pet'].widget = forms.HiddenInput()
        else:
            # Only show available pets in dropdown
            self.fields['pet'].queryset = Pet.objects.filter(status='available')
        
        # Make landlord_approval required if renting
        if self.data.get('own_or_rent') == 'rent':
            self.fields['landlord_approval'].required = True
        
        # Make other_pets_description required if has_other_pets is checked
        if self.data.get('has_other_pets'):
            self.fields['other_pets_description'].required = True
    
    def clean_phone(self):
        """Validate phone number format."""
        phone = self.cleaned_data.get('phone')
        if phone:
            # Remove common formatting characters
            cleaned_phone = ''.join(filter(str.isdigit, phone))
            if len(cleaned_phone) < 10:
                raise ValidationError('Please enter a valid phone number with at least 10 digits.')
        return phone
    
    def clean_email(self):
        """Validate email and check for duplicates."""
        email = self.cleaned_data.get('email')
        if email:
            # Check if there's already a pending application with this email for the same pet
            if self.instance.pk is None:  # Only for new applications
                pet = self.cleaned_data.get('pet') or self.initial.get('pet')
                if pet:
                    existing = AdoptionApplication.objects.filter(
                        email=email,
                        pet=pet,
                        status='pending'
                    ).exists()
                    if existing:
                        raise ValidationError(
                            'You already have a pending application for this pet. '
                            'Please wait for a response before submitting another application.'
                        )
        return email
    
    def clean_household_adults(self):
        """Validate number of adults."""
        adults = self.cleaned_data.get('household_adults')
        if adults and adults < 1:
            raise ValidationError('There must be at least 1 adult in the household.')
        return adults
    
    def clean(self):
        """
        Perform cross-field validation.
        """
        cleaned_data = super().clean()
        
        # Validate landlord approval if renting
        own_or_rent = cleaned_data.get('own_or_rent')
        landlord_approval = cleaned_data.get('landlord_approval')
        
        if own_or_rent == 'rent' and not landlord_approval:
            self.add_error(
                'landlord_approval',
                'Landlord approval is required if you are renting.'
            )
        
        # Validate other pets description if has_other_pets is True
        has_other_pets = cleaned_data.get('has_other_pets')
        other_pets_description = cleaned_data.get('other_pets_description')
        
        if has_other_pets and not other_pets_description:
            self.add_error(
                'other_pets_description',
                'Please describe your other pets.'
            )
        
        # Validate previous pet experience
        previous_pet_experience = cleaned_data.get('previous_pet_experience')
        if previous_pet_experience and len(previous_pet_experience.strip()) < 20:
            self.add_error(
                'previous_pet_experience',
                'Please provide more detail about your previous pet experience (at least 20 characters).'
            )
        
        # Validate reason for adoption
        reason_for_adoption = cleaned_data.get('reason_for_adoption')
        if reason_for_adoption and len(reason_for_adoption.strip()) < 30:
            self.add_error(
                'reason_for_adoption',
                'Please provide more detail about why you want to adopt (at least 30 characters).'
            )
        
        return cleaned_data


class QuickAdoptionApplicationForm(forms.ModelForm):
    """
    Simplified adoption application form for quick inquiries.
    
    This form collects basic information and can be used for initial interest.
    """
    
    class Meta:
        model = AdoptionApplication
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone',
            'pet',
            'reason_for_adoption',
        ]
        
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First Name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone'
            }),
            'pet': forms.HiddenInput(),
            'reason_for_adoption': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Why are you interested in this pet?'
            }),
        }


class ApplicationStatusFilterForm(forms.Form):
    """
    Form for filtering adoption applications in admin dashboard.
    """
    
    STATUS_CHOICES = [
        ('', 'All Statuses'),
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Adoption Completed'),
    ]
    
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by applicant name, email, or pet name...'
        })
    )
    
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )


class ApplicationNotesForm(forms.ModelForm):
    """
    Form for admin to add notes to an application.
    """
    
    class Meta:
        model = AdoptionApplication
        fields = ['notes']
        
        widgets = {
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Add notes about this application...'
            })
        }
        
        labels = {
            'notes': 'Admin Notes'
        }


class ApplicationStatusForm(forms.ModelForm):
    """
    Form for updating application status.
    """
    
    class Meta:
        model = AdoptionApplication
        fields = ['status']
        
        widgets = {
            'status': forms.Select(attrs={
                'class': 'form-select'
            })
        }