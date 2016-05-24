import urllib.request
import csv
import os
import sys
import django

sys.path.append(os.path.abspath(os.path.join('/'.join(__file__.split('/')[:-1]), os.pardir)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finmonopolet.settings')

django.setup()

from product.models import Product
from category.models import Category


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


def product_info_to_product(product_info):
    category_name = read_string(product_info['Varetype'])

    try:
        category = Category.objects.get(name=category_name)
    except Category.DoesNotExist:
        category = Category.objects.create(name=category_name)

    litre_price = read_float(product_info['Literpris'])
    alcohol = read_float(product_info['Alkohol'])

    if alcohol == 0.0:
        alcohol_price = -1
    else:
        alcohol_price = litre_price / alcohol

    return {
        'product_number': read_integer(product_info['Varenummer']),
        'product_name': read_string(product_info['Varenavn']),

        'url': read_string(product_info['Vareurl']),

        'volume': read_float(product_info['Volum']),
        'price': read_float(product_info['Pris']),
        'litre_price': litre_price,
        'alcohol_price': alcohol_price,

        'category': category,

        'fullness': read_integer(product_info['Fylde'], True),
        'freshness': read_integer(product_info['Friskhet'], True),
        'tannins': read_integer(product_info['Garvestoffer'], True),
        'bitterness': read_integer(product_info['Bitterhet'], True),
        'sweetness': read_integer(product_info['Sodme'], True),

        'color': read_string(product_info['Farge'], True),
        'smell': read_string(product_info['Lukt'], True),
        'taste': read_string(product_info['Smak'], True),

        'country': product_info['Land'],
        'district': read_string(product_info['Distrikt'], True),
        'sub_district': read_string(product_info['Underdistrikt'], True),

        'vintage': read_integer(product_info['Argang'], True),

        'feedstock': read_string(product_info['Rastoff'], True),
        'production_method': read_string(product_info['Metode'], True),

        'alcohol': alcohol,
        'sugar': read_float(product_info['Sukker'], True),
        'acid': read_float(product_info['Syre'], True),

        'storage': read_string(product_info['Lagringsgrad'], True),

        'producer': read_string(product_info['Produsent'], True),
        'wholesaler': read_string(product_info['Grossist'], True),
        'distributor': read_string(product_info['Distributor'], True),

        'packaging': product_info['Emballasjetype'],
        'cork': read_string(product_info['Korktype'], True),
    }


def update_database():
    """
    Fetch remote database from vinmonopolet.no. Parse the data and update local database.
    """
    with urllib.request.urlopen('http://www.vinmonopolet.no/api/produkter') as f:
        f = f.read().decode('iso-8859-1').split('\r\n')

        for product_info in csv.DictReader(f[1:], delimiter=';', fieldnames=f[0].split(';')):
            product_info = product_info_to_product(product_info)

            try:
                product = Product.objects.get(product_number=product_info['product_number'])

                for key, value in product_info.items():
                    setattr(product, key, value)

                product.save()
            except Product.DoesNotExist:
                Product.objects.create(**product_info)


if __name__ == '__main__':
    update_database()
