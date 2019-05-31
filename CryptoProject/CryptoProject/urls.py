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
                


#urlpatterns = [path('', views.HomeView.as_view(), name='home'),
#    path('register', views.RegisterView.as_view(), name='register'),
#    path('rphonesend', views.PhoneCreateRView.as_view(), name='rphonesend'),
#    path('orders', views.ordersList, name="orders"),
#    path('welcome', views.welcome, name="welcome"),
#    path('ordersPainter', views.ordersPainter, name="ordersPainter"),
#    path('welcomePainter', views.welcomePainter, name="welcomePainter"),
#    path('newOrder', views.newOrder, name="newOrder"),
#    path('viewOrder', views.viewOrder, name="viewOrder"),
#    path('order_generated_pdf', views.generar_orden, name='order_report_pdf'),
#    path('newDeliver', views.newDeliver, name="newDeliver"),
#    path('newOrder', views.newOrder, name="newOrder"),] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
