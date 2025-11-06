from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # App URLs
    path('', include('apps.pets.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('adoptions/', include('apps.adoptions.urls')),
    path('contact/', include('apps.contact.urls')),
    path('dashboard/', include('apps.dashboard.urls')),
]

# Serve media/static in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)