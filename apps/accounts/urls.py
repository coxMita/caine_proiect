"""
Accounts app URLs.
"""

from django.urls import path, include
from . import views

app_name = 'accounts'

urlpatterns = [
    # Custom login view
    path('login/', views.CustomLoginView.as_view(), name='login'),
    
    # Registration
    path('register/', views.register, name='register'),
    
    # Logout
    path('logout/', views.custom_logout, name='logout'),
    
    # Account management
    path('account/', views.account, name='account'),
    path('applications/', views.user_applications, name='applications'),
    path('edit/', views.edit_profile, name='edit_profile'),
    
    # Django auth URLs (password reset, etc.)
    path('', include('django.contrib.auth.urls')),
]