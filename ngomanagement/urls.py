"""
URL configuration for ngomanagement project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('django-admin/', admin.site.urls),  # Moved Django admin to different path
    path('', include('core.urls')),
]

