"""
Pets app URLs.
"""

from django.urls import path
from . import views

app_name = 'pets'

urlpatterns = [
    # Homepage
    path('', views.home, name='home'),
    
    # Pet pages
    path('pets/', views.PetListView.as_view(), name='list'),
    path('pet/<int:pk>/<slug:slug>/', views.PetDetailView.as_view(), name='detail'),
    
    # Information pages
    path('about/', views.about, name='about'),
    path('success-stories/', views.success_stories, name='success_stories'),
]