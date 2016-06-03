from django.db.models import Count

from rest_framework import serializers, viewsets

from finmonopolet.api import SharedAPIRootRouter
from category.models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', )


class CategoryListSerializer(CategorySerializer):
    number_of_products = serializers.IntegerField()

    class Meta(CategorySerializer.Meta):
        fields = ('id', 'name', 'number_of_products', )


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.annotate(
        number_of_products=Count('products'),
    ).filter(
        number_of_products__gt=0
    )

    pagination_class = None

    ordering_fields = ('canonical_name', 'number_of_products', )
    search_fields = ('canonical_name', )

    def get_serializer_class(self):
        if self.action == 'list':
            return CategoryListSerializer
        elif self.action == 'retrieve':
            return CategorySerializer
        else:
            return CategorySerializer


SharedAPIRootRouter().register(r'categories', CategoryViewSet)
