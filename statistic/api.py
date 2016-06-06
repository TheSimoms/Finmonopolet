from django.db.models import Avg, Count, Sum, Max

from rest_framework import viewsets
from rest_framework.response import Response

from finmonopolet.api import SharedAPIRootRouter

from product.models import Product, Category


class ProductStatisticViewSet(viewsets.ViewSet):
    def list(self, request):
        filters = {}

        for key, value in request.GET.items():
            filters[key] = value.split(',')[0]

        products = Product.objects.filter(**filters).values(
            'country', 'producer', 'price', 'volume', 'alcohol', 'litre_price', 'alcohol_price', 'vintage',
        )

        ordered_by_price = products.order_by('price')
        ordered_by_volume = products.order_by('volume')
        ordered_by_alcohol_level = products.filter(alcohol_price__isnull=False).order_by('alcohol')
        ordered_by_litre_price = products.order_by('litre_price')
        ordered_by_alcohol_price = products.filter(alcohol_price__isnull=False).order_by('alcohol_price')
        ordered_by_vintage = products.order_by('vintage')

        product_statistics = products.aggregate(
            Count('country', distinct=True), Count('producer', distinct=True),
            Avg('price'), Avg('volume'), Avg('alcohol'), Avg('litre_price'), Avg('alcohol_price'), Avg('vintage')
        )

        data = {
            'number_of_countries': product_statistics['country__count'],
            'number_of_producers': product_statistics['producer__count'],

            'price': {
                'min': ordered_by_price.first(),
                'max': ordered_by_price.last(),
                'average': product_statistics['price__avg'],
            },
            'volume': {
                'min': ordered_by_volume.first(),
                'max': ordered_by_volume.last(),
                'average': product_statistics['volume__avg'],
            },
            'alcohol': {
                'min': ordered_by_alcohol_level.first(),
                'max': ordered_by_alcohol_level.last(),
                'average': product_statistics['alcohol__avg'],
            },
            'litre_price': {
                'min': ordered_by_litre_price.first(),
                'max': ordered_by_litre_price.last(),
                'average': product_statistics['litre_price__avg'],
            },
            'alcohol_price': {
                'min': ordered_by_alcohol_price.first(),
                'max': ordered_by_alcohol_price.last(),
                'average': product_statistics['alcohol_price__avg'],
            },
            'vintage': {
                'max': ordered_by_vintage.last(),
                'average': product_statistics['vintage__avg']
            }
        }

        if 'category' not in filters:
            categories = {}

            for category in Category.objects.all():
                category_statistics = products.filter(category=category.id).aggregate(
                    Count('id', distinct=True),
                    Max('price'), Sum('price'),
                    Max('volume'), Sum('volume'),
                    Max('litre_price'),
                    Max('alcohol_price'),
                )

                category_data = {
                    'name': category.name,
                    'number_of_items': category_statistics['id__count'],

                    'price': {
                        'max': category_statistics['price__max'],
                        'total': category_statistics['price__sum'],
                    },
                    'volume': {
                        'max': category_statistics['volume__max'],
                        'total': category_statistics['volume__sum'],
                    },
                    'litre_price': {
                        'max': category_statistics['litre_price__max'],
                    },
                    'alcohol_price': {
                        'max': category_statistics['alcohol_price__max'],
                    },
                }

                categories[category.id] = category_data

            data['categories'] = categories

        return Response(data=data)


SharedAPIRootRouter().register(r'statistics', ProductStatisticViewSet, base_name='statistics')
