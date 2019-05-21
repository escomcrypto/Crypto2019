"""
Definition of urls for CryptoProject.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth import views as auth_views
from app import forms, views


urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('orders', views.ordersList, name="orders"),
    path('welcome', views.home, name="welcome"),
    path ('newOrder', views.newOrder, name="newOrder"),

]
