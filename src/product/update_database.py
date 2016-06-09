import urllib.request
import csv
import os
import sys
import django
import logging
import math
import datetime

from django.db import IntegrityError, transaction

sys.path.append(os.path.abspath(os.path.join('/'.join(__file__.split('/')[:-1]), os.pardir)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finmonopolet.settings')

django.setup()

from finmonopolet.update_database import (
    read_string, read_float, read_integer, read_store_category
)

from product.models import Product, Category, Country, Producer, Suits


logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


def read_category(value):
    if value is None:
        value = 'Uspesifisert'

    try:
        category = Category.objects.get(name=value)
    except Category.DoesNotExist:
        category = Category.objects.create(name=value)

    return category


def read_suits(value):
    suits = []

    for suit_name in value:
        try:
            suit = Suits.objects.get(name=suit_name)
        except Suits.DoesNotExist:
            suit = Suits.objects.create(name=suit_name)

        suits.append(suit)

    return suits


def read_country(value):
    try:
        country = Country.objects.get(name=value)
    except Country.DoesNotExist:
        country = Country.objects.create(name=value)

    return country


def read_producer(value):
    if value is None:
        value = 'Ukjent'

    try:
        producer = Producer.objects.get(name=value)
    except Producer.DoesNotExist:
        producer = Producer.objects.create(name=value)

    return producer


def product_info_to_product(product_info):
    litre_price = read_float(product_info['Literpris'])
    alcohol = read_float(product_info['Alkohol'])

    vintage = read_integer(product_info['Argang'], True)

    if vintage is None:
        vintage = datetime.date.today().year

    if alcohol == 0.0:
        # FIXME: Un-hack this
        alcohol_price = 99999.9
    else:
        alcohol_price = litre_price / alcohol

    active = read_string(product_info['Produktutvalg']) in [
        'Basisutvalget', 'Partiutvalget', 'Bestillingsutvalget'
    ]

    suits_list = []

    for field_name in ['Passertil01', 'Passertil02', 'Passertil03']:
        value = read_string(product_info[field_name], True)

        if value is not None:
            suits_list.append(value)

    name = read_string(product_info['Varenavn'])

    country = read_country(product_info['Land'])

    return {
        'product_number': read_integer(product_info['Varenummer']),

        'name': name,

        'url': read_string(product_info['Vareurl']),

        'volume': read_float(product_info['Volum']),
        'price': read_float(product_info['Pris']),
        'litre_price': litre_price,
        'alcohol_price': alcohol_price,

        'category': read_category(read_string(product_info['Varetype'], True)),

        'fullness': read_integer(product_info['Fylde'], True),
        'freshness': read_integer(product_info['Friskhet'], True),
        'tannins': read_integer(product_info['Garvestoffer'], True),
        'bitterness': read_integer(product_info['Bitterhet'], True),
        'sweetness': read_integer(product_info['Sodme'], True),

        'color': read_string(product_info['Farge'], True),
        'smell': read_string(product_info['Lukt'], True),
        'taste': read_string(product_info['Smak'], True),

        'country': country,
        'district': read_string(product_info['Distrikt'], True),
        'sub_district': read_string(product_info['Underdistrikt'], True),

        'vintage': vintage,

        'feedstock': read_string(product_info['Rastoff'], True),
        'production_method': read_string(product_info['Metode'], True),

        'alcohol': alcohol,
        'sugar': read_float(product_info['Sukker'], True),
        'acid': read_float(product_info['Syre'], True),

        'storage': read_string(product_info['Lagringsgrad'], True),

        'producer': read_producer(read_string(product_info['Produsent'], True)),
        'wholesaler': read_string(product_info['Grossist'], True),
        'distributor': read_string(product_info['Distributor'], True),

        'packaging': product_info['Emballasjetype'],
        'cork': read_string(product_info['Korktype'], True),

        'store_category': read_store_category(product_info['Butikkategori']),

        'active': active,
    }, read_suits(suits_list)


@transaction.atomic()
def update_products():
    """
    Fetch remote product database from vinmonopolet.no. Parse the data and update local database.
    """
    logger.info('Starting product database update')

    with urllib.request.urlopen(
            # FIXME: Change back when redirect is in place. http://www.vinmonopolet.no/api/produkter
            'https://www.vinmonopolet.no/medias/sys_master/products/products/hbc/hb0/8834253127710/produkter.csv'
    ) as f:
        f = f.read().decode('iso-8859-1').split('\r\n')

        logger.info('Remote database read. Updating local database.')

        reader = list(csv.DictReader(f[1:], delimiter=';', fieldnames=f[0].split(';')))

        # Used for logging progress
        number_of_items = len(reader)
        logging_interval = math.ceil(number_of_items / 100)
        i = 0

        for product_info in reader:
            try:
                with transaction.atomic():
                    product_info, suits = product_info_to_product(product_info)
            except IntegrityError:
                continue

            try:
                product = Product.objects.get(product_number=product_info['product_number'])

                product.active = False

                product.suits = suits

                for key, value in product_info.items():
                    setattr(product, key, value)

                product.save()
            except Product.DoesNotExist:
                product = Product.objects.create(**product_info)

                product.suits = suits

                product.save()

            i += 1

            if i % logging_interval == 0:
                logger.info('%.2f%% complete' % int(i / number_of_items * 100))

        logger.info('Database update complete')


if __name__ == '__main__':
    update_products()