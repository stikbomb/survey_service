""" Виды для логина и логаута пользователя. """
from django.contrib.auth import login, logout
from rest_framework import views
from rest_framework.response import Response

from .serializers import UserSerializer, LoginSerializer


class LoginView(views.APIView):
    """ Вид для логина. """
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)

        return Response(UserSerializer(user).data)


class LogoutView(views.APIView):
    """ Вид для логаута. """
    def post(self, request):
        logout(request)

        return Response()
