from rest_framework import serializers, viewsets

from finmonopolet.api import SharedAPIRootRouter
from category.api import CategorySerializer

from product.models import Product


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = '__all__'


class ProductListSerializer(ProductSerializer):
    class Meta(ProductSerializer.Meta):
        fields = (
            'id', 'name', 'category', 'country', 'producer', 'volume', 'price', 'litre_price', 'alcohol_price',
            'alcohol',

        )


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()

    filter_fields = (
        'category', 'country', 'producer',
    )
    ordering_fields = (
        'name', 'category', 'vintage', 'volume', 'price', 'litre_price', 'alcohol_price', 'alcohol',
    )
    search_fields = (
        'name', 'category', 'vintage', 'country', 'producer', 'feedstock', 'wholesaler',
    )

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        elif self.action == 'retrieve':
            return ProductSerializer
        else:
            return ProductSerializer


SharedAPIRootRouter().register(r'products', ProductViewSet)
