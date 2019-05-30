from django.urls import path
 
from . import views

app_name = 'client'
urlpatterns = [
    path('welcome', views.Welcome.as_view(), name='welcome'),
    path('ordersList', views.OrdersList.as_view(), name='ordersList'),
    path('newOrder',views.NewOrder.as_view(),name='newOrder'),
    path('deliversClient',views.DeliversClient.as_view(), name='DeliversClient'),
    path('downloadImage',views.DownloadImage.as_view(),name="downloadImage"),
    path('viewOrder',views.ViewOrder.as_view(), name='viewOrder'),
    path('order_generated_pdf', views.generar_orden, name='order_report_pdf'),
]