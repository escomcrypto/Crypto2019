# two_factor/urls.py
from django.urls import path
 
from . import views
 
app_name = 'users'
urlpatterns = [
    path('login', views.LoginView.as_view(), name='login'),
    path('register', views.RegisterView.as_view(), name='register'),
    path('verifyrcode', views.CodeVerifyRView.as_view(), name='verifyrcode')
]
