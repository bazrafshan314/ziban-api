from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer, ProductSerializer, CategorySerializer
from .models import User, Product, Category, CartItem


class UserRegisterAPIView(generics.CreateAPIView):
    permission_classes = []

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserLoginView(APIView):
    permission_classes = []

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class GetTokenView(APIView):
    permission_classes = []

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            data = {"token": token.key}
        else:
            data = {"message": "invalid username or password"}

        return Response(data)


class ProductViewSet(viewsets.ViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def retrieve(self, request, pk=None):
        product = get_object_or_404(self.queryset, pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    @action(detail=False)
    def category_filter(self, request):
        pk = request.GET.get("category")
        category = Category.objects.get(pk=pk)
        products = Product.objects.filter(category=category)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["POST"])
    def add_to_cart(self, request):
        user = request.user
        pk = request.data.get("product")
        count = request.data.get("count")
        product = get_object_or_404(self.queryset, pk=pk)

        if int(product.inventory) > int(count):
            cart_item = CartItem(user=user, product=product, count=count)
            cart_item.save()
            product.inventory = str(int(product.inventory) - int(count))
            product.save()
            return Response("Done")
        else:
            return Response("Not enough products", status=status.HTTP_400_BAD_REQUEST)


class CategoryViewSet(viewsets.ViewSet):
    serializer_class = CategorySerializer
    queryset = Product.objects.all()

    def list(self, request):
        serializer = CategorySerializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        category = get_object_or_404(self.queryset, pk=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)
