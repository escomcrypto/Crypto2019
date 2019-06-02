"""
Definition of urls for CryptoProject.
"""
from django.conf.urls import include
from app.views import error_404_view, error_500_view, error_400_view, error_403_view

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth import views as auth_views
from app import forms, views, obfuscated, pytransform
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import (
handler400, handler403, handler404, handler500
)

app_name = 'cryptoproject'


handler400 = error_400_view
handler403 = error_403_view
handler404 = error_404_view
handler500 = error_500_view

urlpatterns = [path('', views.HomeView.as_view(), name='home'),
                path('user/', include('users.urls')),
                path('client/',include('client.urls', namespace="client")),
                path('painter/',include('painter.urls', namespace="painter")),] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
