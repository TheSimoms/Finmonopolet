from django.db.models import Count
from rest_framework import serializers, viewsets

from finmonopolet.api import SharedAPIRootRouter
from category.models import Category


class CategorySerializer(serializers.ModelSerializer):
    number_of_products = serializers.IntegerField()

    class Meta:
        model = Category
        fields = ('name', 'number_of_products', )


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.annotate(
            number_of_products=Count('products'),
        )


SharedAPIRootRouter().register(r'categories', CategoryViewSet)
