"""
Pets app URLs.
"""

from django.urls import path
from .. import dashboard

app_name = 'pets'

urlpatterns = [
    # Homepage
    path('', dashboard.home, name='home'),
    
    # Pet pages
    path('pets/', dashboard.PetListView.as_view(), name='list'),
    path('pet/<int:pk>/<slug:slug>/', dashboard.PetDetailView.as_view(), name='detail'),
    
    # Information pages
    path('about/', dashboard.about, name='about'),
    path('success-stories/', dashboard.success_stories, name='success_stories'),
]