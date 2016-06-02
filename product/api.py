import rest_framework_filters as filters

from rest_framework import serializers, viewsets

from finmonopolet.api import SharedAPIRootRouter
from category.api import CategorySerializer
from store.api import StoreCategorySerializer

from product.models import Product, Suits


class SuitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suits
        fields = ('id', 'name', )


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    store_category = StoreCategorySerializer()
    suits = serializers.ListSerializer(child=SuitsSerializer())

    class Meta:
        model = Product
        fields = '__all__'


class ProductListSerializer(ProductSerializer):
    class Meta(ProductSerializer.Meta):
        fields = (
            'id', 'name', 'category', 'country', 'producer', 'volume', 'alcohol', 'price', 'litre_price',
            'alcohol_price',
        )


class SuitsFilter(filters.FilterSet):
    id = filters.AllLookupsFilter(name='id')

    class Meta:
        model = Suits
        fields = ('id', )


class ProductFilter(filters.FilterSet):
    volume = filters.AllLookupsFilter(name='volume')
    alcohol = filters.AllLookupsFilter(name='alcohol')
    price = filters.AllLookupsFilter(name='price')
    litre_price = filters.AllLookupsFilter(name='litre_price')
    alcohol_price = filters.AllLookupsFilter(name='alcohol_price')

    suits = filters.RelatedFilter(SuitsFilter, name='suits')

    class Meta:
        model = Product
        fields = (
            'category', 'country', 'producer', 'store_category', 'suits', 'alcohol', 'volume', 'price',
            'litre_price', 'alcohol_price',
        )


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(active=True)

    filter_class = ProductFilter

    ordering_fields = (
        'canonical_name', 'category', 'country', 'producer', 'volume', 'alcohol', 'price', 'litre_price',
        'alcohol_price',
    )
    search_fields = (
        'canonical_name', 'category__canonical_name', 'vintage', 'country', 'producer', 'feedstock', 'wholesaler',
    )

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        elif self.action == 'retrieve':
            return ProductSerializer
        else:
            return ProductSerializer


SharedAPIRootRouter().register(r'products', ProductViewSet)
