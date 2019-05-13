from django.conf.urls import include, url
from persona.views import inicioSesion, main, ordersList
urlpatterns = [
    url('iniciarSesion', inicioSesion, name='iniciarSesion'),
    url('main', main, name='main'),
    url('ordersList', ordersList, name='orderList'),
]
