"""
Definition of urls for CryptoProject.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.conf.urls import url, include
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views


urlpatterns = [
    path('', views.home, name='home'),
    path('orders', views.ordersList, name="orders"),
    path('welcome', views.home, name="welcome"),
    path ('newOrder', views.newOrder, name="newOrder"),

    #path('contact/', views.contact, name='contact'),
    #path('about/', views.about, name='about'),
    #path('login/',
    #     LoginView.as_view
    #     (
    #         template_name='app/login.html',
    #         authentication_form=forms.BootstrapAuthenticationForm,
    #         extra_context=
    #         {
    #             'title': 'Log in',
    #             'year' : datetime.now().year,
    #         }
    #     ),
    #     name='login'),
    #path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    #path('admin/', admin.site.urls),
]
