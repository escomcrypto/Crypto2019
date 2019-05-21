from django.conf.urls import include, url
from app.views import ordersList

urlpatterns = [
    url('ordersList', ordersList, name='ordersList'),
]