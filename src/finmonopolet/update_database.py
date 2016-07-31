import sys
import os
import logging
import csv

import django

from urllib.request import urlopen


sys.path.append(os.path.abspath(os.path.join('/'.join(__file__.split('/')[:-1]), os.pardir)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finmonopolet.settings')

django.setup()


def read_csv_from_url(url):
    with urlopen(url) as response:
        data = response.read().decode('iso-8859-1').split('\r\n')

        logging.info('Remote database read. Updating local database.')

        return list(csv.DictReader(data[1:], delimiter=';', fieldnames=data[0].split(';')))


def read_value(value, optional=False):
    if len(value) == 0:
        if optional:
            return None
        else:
            raise ValueError('Mandatory value empty!')

    if value in ['Ukjent', '0']:
        return None

    return value


def read_float(value, optional=False):
    value = read_value(value, optional)

    if value is None:
        return None

    return float(value.replace(',', '.'))


def read_integer(value, optional=False):
    value = read_value(value, optional)

    if value is None:
        return None

    return int(value)


def read_string(value, optional=False):
    return read_value(value, optional)


def read_store_category(value):
    from store.models import StoreCategory

    try:
        category_number = int(value[-1])
    except ValueError:
        category_number = 0

    if category_number == 0:
        category_name = 'Uavhengig sortiment'
    else:
        category_name = 'Butikkategori %d' % category_number

    try:
        category = StoreCategory.objects.get(category_number=category_number)
    except StoreCategory.DoesNotExist:
        category = StoreCategory.objects.create(category_number=category_number, name=category_name)

    return category


def update_database():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')

    from product.update_database import update_products
    from store.update_database import update_stores
    from statistic.update_database import update_statistics

    update_products()
    update_stores()
    update_statistics()


if __name__ == '__main__':
    update_database()
