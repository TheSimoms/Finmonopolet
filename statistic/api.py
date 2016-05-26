from django.db.models import Avg, Count, Sum, Max

from rest_framework import serializers, viewsets
from rest_framework.response import Response

from finmonopolet.api import SharedAPIRootRouter

from product.models import Product
from category.models import Category


class ProductStatisticViewSet(viewsets.ViewSet):
    def list(self, request):
        filters = {}

        for key, value in request.GET.items():
            filters['%s__in' % key] = value.split(',')

        products = Product.objects.filter(**filters).values(
            'name', 'country', 'district', 'sub_district', 'producer', 'price', 'volume', 'alcohol', 'litre_price',
            'alcohol_price', 'vintage',
        )

        ordered_by_price = products.order_by('price')
        ordered_by_volume = products.order_by('volume')
        ordered_by_alcohol_level = products.filter(alcohol_price__isnull=False).order_by('alcohol')
        ordered_by_litre_price = products.order_by('litre_price')
        ordered_by_alcohol_price = products.filter(alcohol_price__isnull=False).order_by('alcohol_price')
        ordered_by_vintage = products.order_by('vintage')

        data = {
            'number_of_countries': products.aggregate(Count('country', distinct=True))['country__count'],
            'number_of_producers': products.aggregate(Count('producer', distinct=True))['producer__count'],

            'min_price': ordered_by_price.first(),
            'max_price': ordered_by_price.last(),
            'average_price': ordered_by_price.aggregate(Avg('price'))['price__avg'],

            'min_volume': ordered_by_volume.first(),
            'max_volume': ordered_by_volume.last(),
            'average_volume': ordered_by_volume.aggregate(Avg('volume'))['volume__avg'],

            'average_alcohol_level': ordered_by_alcohol_level.aggregate(Avg('alcohol'))['alcohol__avg'],

            'min_litre_price': ordered_by_litre_price.first(),
            'max_litre_price': ordered_by_litre_price.last(),
            'average_litre_price': ordered_by_litre_price.aggregate(Avg('litre_price'))['litre_price__avg'],

            'min_alcohol_price': ordered_by_alcohol_price.first(),
            'max_alcohol_price': ordered_by_alcohol_price.last(),
            'average_alcohol_price': ordered_by_alcohol_price.aggregate(Avg('alcohol_price'))['alcohol_price__avg'],

            'max_vintage': ordered_by_vintage.last(),
            'average_vintage': ordered_by_vintage.aggregate(Avg('vintage'))['vintage__avg']
        }

        if 'category__in' not in filters:
            categories = {}

            for category in Category.objects.all():
                products = Product.objects.filter(category=category.id).values()

                category_data = {
                    'name': category.name,
                    'number_of_items': products.count(),

                    'max_price': products.aggregate(Max('price'))['price__max'],
                    'total_price': products.aggregate(Sum('price'))['price__sum'],

                    'max_volume': products.aggregate(Max('volume'))['volume__max'],
                    'total_volume': products.aggregate(Sum('volume'))['volume__sum'],

                    'total_alcohol_level': products.aggregate(Sum('alcohol'))['alcohol__sum'],

                    'max_litre_price': products.aggregate(Max('litre_price'))['litre_price__max'],

                    'max_alcohol_price': products.aggregate(Max('alcohol_price'))['alcohol_price__max'],
                }

                categories[category.id] = category_data

            data['categories'] = categories

        return Response(data=data)


SharedAPIRootRouter().register(r'statistics', ProductStatisticViewSet, base_name='statistics')
