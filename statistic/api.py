from django.db.models import Avg, Count, Max, Min

from rest_framework import serializers, viewsets
from rest_framework.response import Response

from finmonopolet.api import SharedAPIRootRouter

from product.models import Product


class ProductStatisticSerializer(serializers.Serializer):
    min_price = serializers.DecimalField(max_digits=8, decimal_places=2)
    max_price = serializers.DecimalField(max_digits=8, decimal_places=2)
    average_price = serializers.DecimalField(max_digits=8, decimal_places=2)

    min_volume = serializers.DecimalField(max_digits=5, decimal_places=2)
    max_volume = serializers.DecimalField(max_digits=5, decimal_places=2)
    average_volume = serializers.DecimalField(max_digits=5, decimal_places=2)

    min_alcohol_level = serializers.DecimalField(max_digits=8, decimal_places=2)
    max_alcohol_level = serializers.DecimalField(max_digits=8, decimal_places=2)
    average_alcohol_level = serializers.DecimalField(max_digits=8, decimal_places=2)

    min_litre_price = serializers.DecimalField(max_digits=8, decimal_places=2)
    max_litre_price = serializers.DecimalField(max_digits=8, decimal_places=2)
    average_litre_price = serializers.DecimalField(max_digits=8, decimal_places=2)

    min_alcohol_price = serializers.DecimalField(max_digits=8, decimal_places=2)
    max_alcohol_price = serializers.DecimalField(max_digits=8, decimal_places=2)
    average_alcohol_price = serializers.DecimalField(max_digits=8, decimal_places=2)

    min_vintage = serializers.DecimalField(max_digits=6, decimal_places=2)
    max_vintage = serializers.DecimalField(max_digits=6, decimal_places=2)
    average_vintage = serializers.DecimalField(max_digits=6, decimal_places=2)

    number_of_objects = Product.objects.count()

    number_of_countries = serializers.IntegerField(min_value=0, max_value=number_of_objects)
    number_of_producers = serializers.IntegerField(min_value=0, max_value=number_of_objects)


class ProductStatisticViewSet(viewsets.ViewSet):
    serializer_class = ProductStatisticSerializer

    def list(self, request):
        return Response(
            Product.objects.all().aggregate(
                min_price=Min('price'),
                max_price=Max('price'),
                average_price=Avg('price'),

                min_volume=Min('volume'),
                max_volume=Max('volume'),
                average_volume=Avg('volume'),

                min_alcohol_level=Min('alcohol'),
                max_alcohol_level=Max('alcohol'),
                average_alcohol_level=Avg('alcohol'),

                min_litre_price=Min('litre_price'),
                max_litre_price=Max('litre_price'),
                average_litre_price=Avg('litre_price'),

                min_alcohol_price=Min('alcohol_price'),
                max_alcohol_price=Max('alcohol_price'),
                average_alcohol_price=Avg('alcohol_price'),

                min_vintage=Min('vintage'),
                max_vintage=Max('vintage'),
                average_vintage=Avg('vintage'),

                number_of_countries=Count('country', distinct=True),
                number_of_producers=Count('producer', distinct=True),
            )
        )


SharedAPIRootRouter().register(r'statistics', ProductStatisticViewSet, base_name='product_statistics')
