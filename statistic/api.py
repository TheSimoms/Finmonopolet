from django.db.models import Avg, Count, Sum, Max

from rest_framework import viewsets
from rest_framework.response import Response

from finmonopolet.api import SharedAPIRootRouter

from product.models import Product
from category.models import Category


class ProductStatisticViewSet(viewsets.ViewSet):
    def list(self, request):
        filters = {}

        for key, value in request.GET.items():
            filters[key] = value.split(',')[0]

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

        product_statistics = products.aggregate(
            Count('country', distinct=True), Count('producer', distinct=True),
            Avg('price'), Avg('volume'), Avg('alcohol'), Avg('litre_price'), Avg('alcohol_price'), Avg('vintage')
        )

        data = {
            'number_of_countries': product_statistics['country__count'],
            'number_of_producers': product_statistics['producer__count'],

            'min_price': ordered_by_price.first(),
            'max_price': ordered_by_price.last(),
            'average_price': product_statistics['price__avg'],

            'min_volume': ordered_by_volume.first(),
            'max_volume': ordered_by_volume.last(),
            'average_volume': product_statistics['volume__avg'],

            'min_alcohol_level': ordered_by_alcohol_level.first(),
            'max_alcohol_level': ordered_by_alcohol_level.last(),
            'average_alcohol_level': product_statistics['alcohol__avg'],

            'min_litre_price': ordered_by_litre_price.first(),
            'max_litre_price': ordered_by_litre_price.last(),
            'average_litre_price': product_statistics['litre_price__avg'],

            'min_alcohol_price': ordered_by_alcohol_price.first(),
            'max_alcohol_price': ordered_by_alcohol_price.last(),
            'average_alcohol_price': product_statistics['alcohol_price__avg'],

            'max_vintage': ordered_by_vintage.last(),
            'average_vintage': product_statistics['vintage__avg']
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

                    'max_price': category_statistics['price__max'],
                    'total_price': category_statistics['price__sum'],

                    'max_volume': category_statistics['volume__max'],
                    'total_volume': category_statistics['volume__sum'],

                    'max_litre_price': category_statistics['litre_price__max'],

                    'max_alcohol_price': category_statistics['alcohol_price__max'],
                }

                categories[category.id] = category_data

            data['categories'] = categories

        return Response(data=data)


class RangeStatisticViewSet(viewsets.ViewSet):
    def list(self, request):
        filters = {}

        for key, value in request.GET.items():
            filters['%s__in' % key] = value.split(',')

        data = {}

        for value, ranges, unit in (
            ('volume', (0.5, 0.75, 1.0, 1.5, 2.0, 3.0), ' l'),
            ('price', (100, 150, 200, 300, 500), ',-'),
            ('alcohol', (5, 10, 20, 30, 45), ' %'),
            ('litre_price', (100, 150, 200, 300, 500), ' kr per l'),
            ('alcohol_price', (10, 15, 20, 30, 40, 55, 60, 75, 100, 150, 200, 500), ' kr per %'),
        ):
            value_filters = dict(filters)

            if ('%s__range' % value) in value_filters:
                del value_filters['%s__range' % value]

            value_products = Product.objects.filter(**value_filters)

            data[value] = [
                {
                    'id': '0,%d' % ranges[0],
                    'name': 'Under %s%s' % (str(ranges[0]), unit),
                    'number_of_products': value_products.filter(**{('%s__lte' % value): ranges[0]}).count()
                }
            ]

            for i in range(1, len(ranges)-1):
                data[value].append(
                    {
                        'id': '%d,%d' % (ranges[i-1], ranges[i]),
                        'name': '%s - %s%s' % (str(ranges[i-1]), str(ranges[i]), unit),
                        'number_of_products': value_products.filter(
                            **{('%s__range' % value): (ranges[i-1], ranges[i])}
                        ).count()
                    }
                )

            data[value].append(
                {
                    'id': '%d,999999' % ranges[-1],  # Un-hack this
                    'name': 'Over %s%s' % (str(ranges[-1]), unit),
                    'number_of_products': value_products.filter(**{('%s__gte' % value): ranges[-1]}).count()
                }
            )

        return Response(data=data)


SharedAPIRootRouter().register(r'statistics/full', ProductStatisticViewSet, base_name='statistics_full')
SharedAPIRootRouter().register(r'statistics/ranges', RangeStatisticViewSet, base_name='statistics_ranges')
