import django_filters

from rest_framework import serializers, viewsets, filters

from finmonopolet.api import SharedAPIRootRouter
from category.api import CategorySerializer

from product.models import Product


class ProductFilter(filters.FilterSet):
    category_name = django_filters.CharFilter(name='category__name')

    class Meta:
        model = Product
        fields = ('category', 'category_name', )


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = '__all__'


class ProductListSerializer(ProductSerializer):
    class Meta(ProductSerializer.Meta):
        fields = ('id', 'name', 'category', 'volume', 'price', 'litre_price', 'alcohol_price', 'alcohol', )


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    filter_class = ProductFilter

    ordering_fields = (
        'name', 'volume', 'price', 'litre_price', 'alcohol_price', 'category', 'vintage', 'alcohol',
    )
    search_fields = (
        'name', 'category', 'vintage', 'country', 'feedstock', 'producer', 'wholesaler',
    )

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        elif self.action == 'retrieve':
            return ProductSerializer
        else:
            return ProductSerializer


SharedAPIRootRouter().register(r'products', ProductViewSet)
