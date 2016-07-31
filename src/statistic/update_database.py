import os
import sys
import django
import logging
import math
import datetime

from operator import add
from collections import defaultdict

from django.db import transaction


sys.path.append(os.path.abspath(os.path.join('/'.join(__file__.split('/')[:-1]), os.pardir)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finmonopolet.settings')

django.setup()


from product.models import Product, Category, Country
from statistic.models import Statistics


def new_statistics_element():
    return {
        'max': None,
        'min': None,
        'avg': 0.0
    }


def new_statistics_collection(item=None):
    statistics = {
        'count': {
            'items': 0,

            'category': defaultdict(int),
            'country': defaultdict(int),
        },

        'volume': new_statistics_element(),
        'price': new_statistics_element(),
        'litre_price': new_statistics_element(),
        'alcohol_price': new_statistics_element(),
        'vintage': new_statistics_element(),
    }

    if isinstance(item, Category):
        statistics['category'] = item
    elif isinstance(item, Country):
        statistics['country'] = item

    return statistics


def update_field(element, value, field, product, operator, data_type):
    field_value = data_type(getattr(product, field))

    element[value] = field_value if element[value] is None else operator(
        element[value], field_value
    )


def update_statistics_element(statistics_collection, field, product, data_type=float):
    statistics_element = statistics_collection[field]

    update_field(statistics_element, 'max', field, product, max, data_type)
    update_field(statistics_element, 'min', field, product, min, data_type)
    update_field(statistics_element, 'avg', field, product, add, data_type)


def update_statistics_collection(statistics_collection, product):
    statistics_collection['count']['items'] += 1

    if 'category' not in statistics_collection:
        statistics_collection['count']['country'][product.country.id] += 1

    if 'country' not in statistics_collection:
        statistics_collection['count']['category'][product.category.id] += 1

    update_statistics_element(statistics_collection, 'volume', product)
    update_statistics_element(statistics_collection, 'price', product)
    update_statistics_element(statistics_collection, 'litre_price', product)
    update_statistics_element(statistics_collection, 'alcohol_price', product)
    update_statistics_element(statistics_collection, 'vintage', product, int)


def collect_statistics():
    # Global statistics
    global_statistics = new_statistics_collection()

    # Statistics per category
    category_statistics = {
        category.id: new_statistics_collection(category)
        for category in Category.objects.only('id')
    }

    # Statistics per country
    country_statistics = {
        country.id: new_statistics_collection(country)
        for country in Country.objects.only('id')
    }

    # Fetch products with relevant fields
    products = Product.objects.only(
        'category', 'country', 'price', 'volume', 'alcohol',
        'litre_price', 'alcohol_price', 'vintage',
    )

    # Used for logging progress
    number_of_items = len(products)
    logging_interval = math.ceil(number_of_items / 100)
    i = 0

    # Iterate all products
    for product in products:
        # Update statistics
        update_statistics_collection(global_statistics, product)
        update_statistics_collection(category_statistics[product.category.id], product)
        update_statistics_collection(country_statistics[product.country.id], product)

        i += 1

        if i % logging_interval == 0:
            logging.info('%.2f%% complete' % int(i / number_of_items * 100))

    fields = ['volume', 'price', 'litre_price', 'alcohol_price', 'vintage']

    # Update average values
    for statistics_dictionary in [category_statistics, country_statistics]:
        for object_id in statistics_dictionary:
            statistics_collection = statistics_dictionary[object_id]

            for field in fields:
                statistics_collection[field]['avg'] /= statistics_collection['count']['items']

            Statistics.objects.create(**statistics_collection)


@transaction.atomic
def update_statistics():
    """
    Collect latest statistics.
    """
    logging.info('Starting statistic database update')

    collect_statistics()

    logging.info('Database update complete')


if __name__ == '__main__':
    update_statistics()
