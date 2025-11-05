"""
Contact app views.
"""

from django.shortcuts import render, redirect
from django.contrib import messages

from .services import ContactMessageService


def contact(request):
    """Contact page view with form submission"""
    if request.method == 'POST':
        # Create contact message using service
        contact_message = ContactMessageService.create_message(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone', ''),
            subject=request.POST.get('subject'),
            message=request.POST.get('message')
        )
        
        messages.success(
            request,
            'Thank you for contacting us! We will get back to you soon.'
        )
        return redirect('contact:contact')
    
    return render(request, 'contact/contact.html')