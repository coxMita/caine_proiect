"""
Dashboard app decorators.
"""

from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def admin_required(view_func):
    """
    Decorator to require admin/staff privileges.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to access this page.')
            return redirect('accounts:login')
        
        if not (request.user.is_staff or request.user.is_superuser):
            messages.error(request, 'You must be an administrator to access this page.')
            return redirect('pets:home')
        
        return view_func(request, *args, **kwargs)
    
    return wrapper  