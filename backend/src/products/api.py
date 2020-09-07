from django.db.models import Count, Q
from django_filters import rest_framework as filters
from rest_framework import serializers, viewsets, pagination

from products.models import Product, ProductType, Country, Producer


class ForeignKeySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class ForeignKeyListSerializer(ForeignKeySerializer):
    number_of_products = serializers.IntegerField()


class ForeignKeyPagination(pagination.PageNumberPagination):
    page_size = 5


class ForeignKeyViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ForeignKeyListSerializer
    pagination_class = ForeignKeyPagination

    ordering_fields = ['sort_name']
    search_fields = ['name']

    def get_queryset(self):
        model_name = self.request.path.split('/')[2]

        if model_name == 'product_types':
            queryset = ProductType
        elif model_name == 'countries':
            queryset = Country
        elif model_name == 'producers':
            queryset = Producer
        else:
            return

        return queryset.objects.annotate(
            number_of_products=Count('products', filter=Q(
                products__active=True,
                products__stock__gt=0,
            )),
        ).filter(
            number_of_products__gt=0
        )


class ProductSerializer(serializers.ModelSerializer):
    product_type = ForeignKeySerializer()
    country = ForeignKeySerializer()
    producer = ForeignKeySerializer()

    class Meta:
        model = Product
        fields = [
            'product_number', 'name', 'alcohol_content', 'volume', 'price',
            'litre_price',  'alcohol_price', 'vintage', 'product_type', 'country',
            'producer', 'last_updated',
        ]


class ProductFilter(filters.FilterSet):
    class ListFilter(filters.BaseInFilter, filters.NumberFilter):
        pass

    product_type = ListFilter(field_name='product_type')
    country = ListFilter(field_name='country')
    producer = ListFilter(field_name='producer')

    class Meta:
        default_filters = ['exact', 'lte', 'gte', 'range']

        model = Product
        fields = {
            'alcohol_content': default_filters,
            'volume': default_filters,
            'price': default_filters,
            'litre_price': default_filters,
            'alcohol_price': default_filters,
            'vintage': default_filters,
        }


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(active=True, stock__gt=0)
    serializer_class = ProductSerializer
    filter_class = ProductFilter

    ordering_fields = [
        'sort_name', 'volume', 'price', 'litre_price', 'alcohol_price', 'alcohol_content',
        'vintage', 'product_type', 'country', 'producer',
    ]
    search_fields = [
        'name', 'product_number', 'vintage', 'product_type__name', 'country__name',
        'producer__name', 'volume', 'price', 'litre_price', 'alcohol_price', 'alcohol_content',
    ]
