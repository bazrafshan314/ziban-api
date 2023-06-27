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
from .serializers import (
    UserSerializer,
    ProductSerializer,
    CategorySerializer,
    BarberSerializer,
)
from .models import (
    User,
    Product,
    Category,
    CartItem,
    Order,
    OrderItem,
    Barber,
    Reservation,
)
from django.views.decorators.csrf import csrf_exempt


class UserRegisterAPIView(generics.CreateAPIView):
    permission_classes = []

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserLoginView(APIView):
    permission_classes = []

    @csrf_exempt
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

    def list(self, request):
        serializer = ProductSerializer(self.queryset, many=True)
        return Response(serializer.data)

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
        count = int(request.data.get("count"))
        product = get_object_or_404(self.queryset, pk=pk)

        if product.inventory - count:
            cart_item = CartItem.objects.create(user=user, product=product, count=count)
            cart_item.save()
            # product.inventory = str(int(product.inventory) - int(count))
            # product.save()
            return Response("Done")
        else:
            return Response("Not enough products", status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["POST"])
    def order(self, request):
        user = request.user
        cart = user.cartitem_set.all()
        address = request.data.get("address")
        order = Order.objects.create(address=address)
        order.save()
        for item in cart:
            if item.product.inventory > item.count:
                order_item = OrderItem(
                    order=order, user=user, product=item.product, count=item.count
                )
                order_item.save()
                item.product.inventory = item.product.inventory - item.count
                item.product.save()
                item.delete()
        if not order.orderitem_set:
            order.delete()
            return Response(
                "Not enough products for any item", status=status.HTTP_400_BAD_REQUEST
            )
        else:
            return Response("Done")


class CategoryViewSet(viewsets.ViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def list(self, request):
        serializer = CategorySerializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        category = get_object_or_404(self.queryset, pk=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)


class BarberViewSet(viewsets.ViewSet):
    serializer_class = BarberSerializer
    queryset = Barber.objects.all()

    def list(self, request):
        serializer = BarberSerializer(self.queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["POST"])
    def reserve(self, request):
        user = request.user
        pk = request.data.get("barber")
        time = request.data.get("time")
        barber = get_object_or_404(self.queryset, pk=pk)

        reservation = Reservation.objects.create(user=user, barber=barber, time=time)
        reservation.save()

        return Response("Done")
