import django_filters

from rest_framework import serializers, viewsets, filters

from finmonopolet.api import SharedAPIRootRouter

from product.models import Product
from category.models import Category


class ProductFilter(filters.FilterSet):
    category_name = django_filters.CharFilter(name='category__name')

    class Meta:
        model = Product
        fields = ('category', 'category_name', )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', )


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Product


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
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
