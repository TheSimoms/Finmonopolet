from rest_framework import serializers, viewsets

from products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'product_number', 'name'
        ]


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(active=True)
    serializer_class = ProductSerializer

    ordering_fields = [
        'sort_name',
    ]
    search_fields = [
        'name', 'product_number',
    ]
