from django.urls import path
from . import views

app_name = 'camera'

urlpatterns = [
    path('', views.camera_view, name='index'),
    path('<uuid:pk>/', views.camera_detail, name='detail'),
]
