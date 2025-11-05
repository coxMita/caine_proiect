"""
Core mixins module.
Contains reusable view mixins.
"""

from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect


class AdminRequiredMixin(UserPassesTestMixin):
    """
    Mixin that requires user to be staff/admin.
    """
    def test_func(self):
        return self.request.user.is_authenticated and (
            self.request.user.is_staff or self.request.user.is_superuser
        )
    
    def handle_no_permission(self):
        messages.error(self.request, 'You must be an administrator to access this page.')
        return redirect('pets:home')


class MessageMixin:
    """
    Mixin that provides helper methods for adding messages.
    """
    def add_success_message(self, message):
        messages.success(self.request, message)
    
    def add_error_message(self, message):
        messages.error(self.request, message)
    
    def add_info_message(self, message):
        messages.info(self.request, message)
    
    def add_warning_message(self, message):
        messages.warning(self.request, message)