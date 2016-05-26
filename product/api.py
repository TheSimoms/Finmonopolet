import django_filters

from rest_framework import serializers, viewsets, filters

from finmonopolet.api import SharedAPIRootRouter
from product.models import Product


class ProductFilter(filters.FilterSet):
    category_name = django_filters.CharFilter(name='category__name')

    class Meta:
        model = Product
        fields = ('category', 'category_name', )


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()

    class Meta:
        model = Product


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()

    serializer_class = ProductSerializer
    filter_class = ProductFilter

    ordering_fields = (
        'name', 'volume', 'price', 'litre_price', 'alcohol_price', 'category', 'vintage', 'alcohol',
    )
    search_fields = (
        'name', 'category', 'vintage', 'country', 'feedstock', 'producer', 'wholesaler',
    )


SharedAPIRootRouter().register(r'products', ProductViewSet)
