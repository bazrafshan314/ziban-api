from django.contrib.auth import authenticate
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer
from .models import User


class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GetTokenView(APIView):
    permission_classes = []

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            data = {"token": token.key}
        else:
            data = {"message": "invalid username or password"}

        return Response(data)
