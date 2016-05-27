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
    queryset = Category.objects.all()

    ordering_fields = ('name', 'number_of_products', )

    def get_serializer_class(self):
        if self.action == 'list':
            return CategoryListSerializer
        elif self.action == 'retrieve':
            return CategorySerializer
        else:
            return CategorySerializer

    def get_queryset(self):
        return Category.objects.annotate(
            number_of_products=Count('products'),
        )


SharedAPIRootRouter().register(r'categories', CategoryViewSet)
