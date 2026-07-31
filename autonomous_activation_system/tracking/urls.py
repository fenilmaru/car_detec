from django.urls import path
from . import views

app_name = 'tracking'

urlpatterns = [
    path('', views.tracking_view, name='index'),
    path('routes/', views.route_history_view, name='routes'),
]
