#!/usr/bin/env python3

import logging
import math

from django.db import transaction

from products.models import Product
from utils.vinmonopolet import fetch_url_json_batched


def run(*args):
    logging.basicConfig(level=logging.INFO)

    logging.info('Starting product database update.')

    _update_product_information()

    logging.info('Database update complete.')


def _update_product_information():
    logging.info('Updating product information.')

    products = fetch_url_json_batched(
        'https://apis.vinmonopolet.no/products/v0/details-normal',
        max_results=500
    )

    logging.info('Reading products into the local database.')

    number_of_products = len(products)
    logging_interval = math.ceil(number_of_products / 100)

    # Mark all products as inactive
    with transaction.atomic():
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
def _update_product(product_json):
    product_info = _parse_product_json(product_json)

    if product_info is None:
        return

    Product.objects.update_or_create(
        product_number=product_info['product_number'], defaults=product_info,
    )


def _parse_product_json(product_info):
    name = product_info['basic']['productShortName']

    if not name:
        return
    
    return {
        'product_number': product_info['basic']['productId'],
        'name': name,

        'active': True,
    }
