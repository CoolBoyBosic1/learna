# mainapp/auth_views.py

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, ProfileSerializer

User = get_user_model()

# -----------------------------
# 1) Реєстрація нового користувача
# -----------------------------
class RegisterUserAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        # Генеруємо JWT-токени одразу після створення
        user = User.objects.get(email=response.data['email'])
        refresh = RefreshToken.for_user(user)
        response.data['refresh'] = str(refresh)
        response.data['access'] = str(refresh.access_token)
        return response

# -----------------------------
# 2) Профіль користувача (отримати/оновити)
# -----------------------------
class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    """
    - GET /api/profile/    -> Повертає дані профілю поточного користувача,
                              включно з масивами friends та teachers.
    - PUT/PATCH /api/profile/ -> Дозволяє оновити поля (city, info тощо).
    """
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Повертаємо поточного користувача
        return self.request.user
