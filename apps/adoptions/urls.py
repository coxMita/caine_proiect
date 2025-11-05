"""
Adoptions app URLs.
"""

from django.urls import path
from . import views

app_name = 'adoptions'

urlpatterns = [
    # Adoption process info
    path('process/', views.adoption_process, name='process'),
    
    # Adoption gate (login/register prompt)
    path('start/', views.adoption_gate, name='gate'),
    path('start/<int:pet_id>/', views.adoption_gate, name='gate_pet'),
    
    # Application form
    path('apply/', views.adoption_application, name='application'),
    path('apply/<int:pet_id>/', views.adoption_application, name='application_pet'),
]