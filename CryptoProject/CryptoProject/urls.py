"""
Definition of urls for CryptoProject.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from app import forms, views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('orders', views.ordersList, name="orders"),
    path('welcome', views.welcome, name="welcome"),
    path('ordersPainter', views.ordersPainter, name="ordersPainter"),
    path('welcomePainter', views.welcomePainter, name="welcomePainter"),
    path('newOrder', views.newOrder, name="newOrder"),
    path('newDeliver', views.newDeliver, name="newDeliver"),
    path('order_generated_pdf/$', login_required(views.OrdersGenerationPDF.as_view()), name='order_report_pdf'),
    path('newOrder', views.newOrder, name="newOrder"),] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
