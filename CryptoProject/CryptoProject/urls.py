"""
Definition of urls for CryptoProject.
"""
from django.conf.urls import include

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


#handler400 = views.bad_request
#handler403 = views.permission_denied
handler404 = 'app.views.handler404'
#handler500 = views.server_error

urlpatterns = [path('', views.HomeView.as_view(), name='home'),
                path('user/', include('users.urls')),
                path('client/',include('client.urls', namespace="client")),
                path('painter/',include('painter.urls', namespace="painter")),] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
