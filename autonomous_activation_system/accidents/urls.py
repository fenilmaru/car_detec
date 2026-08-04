from django.urls import path
from . import views

app_name = 'accidents'

urlpatterns = [
    path('', views.accident_list, name='list'),
    path('<uuid:pk>/', views.accident_detail, name='detail'),
]
