from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Category, Product, Cart


class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=20, required=True)
    username = serializers.CharField(max_length=20, required=True)
    password = serializers.CharField(min_length=5, max_length=30, required=True)

    class Meta:
        model = User
        fields = ['first_name', 'username']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class ProductSerializer(serializers.ModelSerializer):
    # category = serializers.SerializerMethodField(method_name='get_category_id', read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'stock', 'category']

    def get_category(self):
        return self.category_id.name


class CartSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(min_value=1)

    class Meta:
        model = Cart
        fields = ['item', 'quantity']

    def to_representation(self, instance):
        return {
            'name': instance.item.name,
            'price': instance.item.price,
            'quantity': instance.quantity
        }

    def validate(self, attrs):
        try:
            product = Product.objects.get(id=attrs['item'])
        except Exception as e:
            return ValidationError("Product does not exist")

        if attrs['quantity'] > product.stock:
            return ValidationError("Item quantity can't be greater than stock quantity")
        super(CartSerializer, self).validate(attrs)
