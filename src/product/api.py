import rest_framework_filters as filters

from django_filters.fields import Lookup

from rest_framework import serializers, viewsets

from finmonopolet.api import SharedAPIRootRouter, ForeignKeyViewSet, ForeignKeySerializer
from store.api import StoreCategorySerializer

from product.models import Product


class ProductSerializer(serializers.ModelSerializer):
    category = ForeignKeySerializer()
    country = ForeignKeySerializer()
    producer = ForeignKeySerializer()
    selection = ForeignKeySerializer()

    store_category = StoreCategorySerializer()

    suits = serializers.ListSerializer(child=ForeignKeySerializer())

    class Meta:
        model = Product
        fields = '__all__'


class ProductListSerializer(ProductSerializer):
    class Meta(ProductSerializer.Meta):
        fields = (
            'id', 'name', 'category', 'country', 'producer',
            'volume', 'alcohol', 'price', 'litre_price', 'alcohol_price'
        )


class ListFilter(filters.Filter):
    def filter(self, queryset, value):
        return super(ListFilter, self).filter(queryset, Lookup(value.split(u','), 'in')).distinct()


class ProductFilter(filters.FilterSet):
    category = ListFilter(name='category')
    country = ListFilter(name='country')
    producer = ListFilter(name='producer')
    store_category = ListFilter(name='store_category')
    suits = ListFilter(name='suits')
    selection = ListFilter(name='selection')

    volume = filters.AllLookupsFilter(name='volume')
    alcohol = filters.AllLookupsFilter(name='alcohol')
    price = filters.AllLookupsFilter(name='price')
    litre_price = filters.AllLookupsFilter(name='litre_price')
    alcohol_price = filters.AllLookupsFilter(name='alcohol_price')

    class Meta:
        model = Product
        fields = (
            'category', 'country', 'producer', 'store_category', 'suits', 'selection',
            'volume', 'alcohol', 'price', 'litre_price', 'alcohol_price',
        )


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(active=True)

    filter_class = ProductFilter

    ordering_fields = (
        'canonical_name', 'category', 'country', 'producer', 'volume', 'alcohol', 'price', 'litre_price',
        'alcohol_price',
    )
    search_fields = (
        'canonical_name', 'category__canonical_name', 'vintage', 'country__canonical_name', 'producer__canonical_name',
        'feedstock', 'wholesaler',
    )

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        elif self.action == 'retrieve':
            return ProductSerializer
        else:
            return ProductSerializer


SharedAPIRootRouter().register(r'products', ProductViewSet, base_name='products')

SharedAPIRootRouter().register(r'categories', ForeignKeyViewSet, base_name='categories')
SharedAPIRootRouter().register(r'countries', ForeignKeyViewSet, base_name='countries')
SharedAPIRootRouter().register(r'producers', ForeignKeyViewSet, base_name='producers')
SharedAPIRootRouter().register(r'suits', ForeignKeyViewSet, base_name='suits')
SharedAPIRootRouter().register(r'selections', ForeignKeyViewSet, base_name='selections')
