from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import api_views

app_name = 'api_auth'

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/', api_views.UserListCreateAPIView.as_view(), name='user-list-create'),
    path('users/<uuid:pk>/', api_views.UserRetrieveUpdateAPIView.as_view(), name='user-detail'),
    path('roles/', api_views.RoleListCreateAPIView.as_view(), name='role-list'),
    path('roles/<uuid:pk>/', api_views.RoleRetrieveUpdateDestroyAPIView.as_view(), name='role-detail'),
    path('profile/', api_views.ProfileAPIView.as_view(), name='profile'),
]
