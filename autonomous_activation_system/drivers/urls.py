from django.urls import path
from . import views

app_name = 'drivers'

urlpatterns = [
    path('', views.driver_dashboard, name='dashboard'),
    path('<uuid:pk>/', views.driver_detail, name='detail'),
]
