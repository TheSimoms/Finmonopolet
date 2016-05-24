from rest_framework import serializers, viewsets

from finmonopolet.api import SharedAPIRootRouter
from product.models import Product


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()

    class Meta:
        model = Product


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_fields = ('category', )
    ordering_fields = (
        'product_name', 'volume', 'price', 'litre_price', 'alcohol_price', 'category', 'vintage', 'alcohol',
    )
    search_fields = (
        'product_name', 'category', 'vintage', 'country', 'feedstock', 'producer', 'wholesaler',
    )


SharedAPIRootRouter().register(r'products', ProductViewSet)
