from rest_framework import routers

from products.api import ProductViewSet, ForeignKeyViewSet

product_router = routers.DefaultRouter()

product_router.register(r'products', ProductViewSet)
product_router.register(r'product_types', ForeignKeyViewSet, basename='product_types')
product_router.register(r'countries', ForeignKeyViewSet, basename='countries')
product_router.register(r'producers', ForeignKeyViewSet, basename='producers')
