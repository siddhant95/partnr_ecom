from rest_framework import routers
from django.urls import path
from .views import UserSignup, CategoryViewSet, ProductViewSet, CartViewSet

router = routers.DefaultRouter()

urlpatterns = [
    path('user/signup/', UserSignup, name='user_signup'),
]


router.register(r'category', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'cart', CartViewSet, basename='cart')

urlpatterns += router.get_urls()
