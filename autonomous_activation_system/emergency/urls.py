from django.urls import path
from . import views

app_name = 'emergency'

urlpatterns = [
    path('', views.emergency_view, name='index'),
    path('contacts/', views.sos_contacts, name='contacts'),
]
