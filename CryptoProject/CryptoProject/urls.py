"""
Definition of urls for CryptoProject.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth import views as auth_views
from app import forms, views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('orders', views.ordersList, name="orders"),
    path('welcome', views.welcome, name="welcome"),
    path ('newOrder', views.newOrder, name="newOrder"),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
