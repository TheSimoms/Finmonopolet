#!/usr/bin/env python3

import logging
import math

from django.db import transaction

from products.models import Product, ProductType, Country, Producer
from utils.vinmonopolet import fetch_url_json_batched


def run():
    logging.basicConfig(level=logging.INFO)

    logging.info('Starting product database update.')

    _update_product_information()
    _update_product_stock()

    logging.info('Database update complete.')


def _update_product_information():
    logging.info('Updating product information.')

    products = fetch_url_json_batched(
        'https://apis.vinmonopolet.no/products/v0/details-normal',
    )

    logging.info('Reading products into the local database.')

    number_of_products = len(products)
    logging_interval = math.ceil(number_of_products / 100)

    # Mark all products as inactive
    Product.objects.update(active=False)

    for i, product in enumerate(products):
        try:
            _update_product(product)
        except Exception as e:
            logging.error('An error occurred when parsing a product. Reason:')
            logging.exception(e)

        if i % logging_interval == 0:
            logging.info('%.2f%% complete' % int(i / number_of_products * 100))


@transaction.atomic
def _update_product_stock():
    logging.info('Updating product stock.')

    product_stock = fetch_url_json_batched(
        'https://apis.vinmonopolet.no/products/v0/accumulated-stock',
        max_results=30000,
    )

    logging.info('Reading product stock into the local database.')

    number_of_products = len(product_stock)
    logging_interval = math.ceil(number_of_products / 100)

    for i, product in enumerate(product_stock):
        Product.objects.filter(
            product_number=product['productId'],
        ).update(
            stock=product['stock'],
        )

        if i % logging_interval == 0:
            logging.info('%.2f%% complete' % int(i / number_of_products * 100))


@transaction.atomic
def _update_product(product_json):
    product_info = _parse_product_json(product_json)

    if product_info is None:
        return

    Product.objects.update_or_create(
        product_number=product_info['product_number'], defaults=product_info,
    )


def _parse_product_json(product_info):
    alcohol_content = _optional_value(
        product_info['basic']['alcoholContent'],
        comparator=lambda x: x > 1.0,
    )

    if not _optional_value(product_info['prices']) or not alcohol_content:
        return

    litre_price = product_info['prices'][0]['salesPricePrLiter']

    return {
        'product_number': product_info['basic']['productId'],

        'name': product_info['basic']['productLongName'],
        'volume': product_info['basic']['volume'],
        'price': product_info['prices'][0]['salesPrice'],
        'litre_price': litre_price,
        'alcohol_price': litre_price / alcohol_content,
        'vintage': _optional_value(product_info['basic']['vintage']),
        'alcohol_content': alcohol_content,

        'product_type': _foreign_key(
            product_info['classification']['subProductTypeName'],
            ProductType,
            'Uspesifisert'
        ),
        'country': _foreign_key(
            product_info['origins']['origin']['country'],
            Country
        ),
        'producer': _foreign_key(
            product_info['logistics']['manufacturerName'],
            Producer
        ),

        'active': True,
    }


def _optional_value(value, comparator=lambda x: x):
    if not comparator(value):
        return None

    return value


def _foreign_key(value, model, no_value='Ukjent'):
    if not value:
        value = no_value

    try:
        item = model.objects.get(name=value)
    except model.DoesNotExist:
        item = model.objects.create(name=value)

    return item
