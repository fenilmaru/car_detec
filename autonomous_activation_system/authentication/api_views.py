from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .serializers import (
    UserSerializer, UserCreateSerializer, RoleSerializer,
    UserProfileSerializer, PasswordChangeSerializer
)
from .models import Role, UserProfile

User = get_user_model()

class UserListCreateAPIView(generics.ListCreateAPIView):
    queryset = User.objects.select_related('role').all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    search_fields = ['username', 'email', 'first_name', 'last_name']

    def get_serializer_class(self):
        return UserCreateSerializer if self.request.method == 'POST' else UserSerializer

class UserRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.select_related('role')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

class RoleListCreateAPIView(generics.ListCreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [permissions.IsAdminUser]

class RoleRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [permissions.IsAdminUser]

class ProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        profile, _ = UserProfile.objects.get_or_create(user=self.request.user)
        return profile
