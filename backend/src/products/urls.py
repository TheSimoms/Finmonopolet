from rest_framework import routers

from products.api import ProductViewSet

product_router = routers.DefaultRouter()

product_router.register(r'products', ProductViewSet)
