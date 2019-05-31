from django.urls import path
 
from . import views

app_name = 'painter'
urlpatterns = [
    path('welcomePainter', views.WelcomePainter.as_view(), name='welcomePainter'),
    path('ordersPainter', views.OrdersPainter.as_view(), name='ordersPainter'),
    path('newDeliver',views.NewDeliver.as_view(),name='newDeliver'),
    path('deliversPainter',views.DeliversPainter.as_view(), name='deliversPainter'),
    path('downloadImage',views.DownloadImage.as_view(),name="downloadImage"),
    path('viewOrder',views.ViewOrder.as_view(), name='viewOrder'),
    path('logoutPainter', views.LogoutView.as_view(), name='logoutPainter'),
]