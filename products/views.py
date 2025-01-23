from django.http import HttpResponse
from django.contrib.auth.models import User

from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
# Create your views here.
from .models import Category, Product, Cart
from .serializers import UserSerializer, CategorySerializer, ProductSerializer, CartSerializer


class UserSignup(mixins.CreateModelMixin):
    def create(self, request, *args, **kwargs):
        serializer = UserSerializer(data=self.request.body)
        if serializer.is_valid():
            u = User.objects.create(
                first_name=serializer.validated_data['first_name'],
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
        return HttpResponse(status=201)


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = (IsAuthenticated,)


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(is_approved=True)
    permission_classes = (IsAuthenticated,)


class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Cart.objects.filter(user_id=self.request.user.id)
