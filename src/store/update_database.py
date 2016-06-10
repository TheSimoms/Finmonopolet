import urllib.request
import csv
import os
import sys
import django
import logging
import math

from django.db import transaction


sys.path.append(os.path.abspath(os.path.join('/'.join(__file__.split('/')[:-1]), os.pardir)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finmonopolet.settings')

django.setup()


from finmonopolet.update_database import read_string, read_float, read_integer, read_store_category

from store.models import Store


def store_info_to_store(store_info):
    opening_times = {
        'week_number': read_integer(store_info['Ukenummer']),

        'monday': read_string(store_info['Apn_mandag']),
        'tuesday': read_string(store_info['Apn_tirsdag']),
        'wednesday': read_string(store_info['Apn_onsdag']),
        'thursday': read_string(store_info['Apn_torsdag']),
        'friday': read_string(store_info['Apn_fredag']),
        'saturday': read_string(store_info['Apn_lordag']),
    }
    opening_times_next = {
        'week_number': read_integer(store_info['Ukenummer_neste']),

        'monday': read_string(store_info['Apn_neste_mandag']),
        'tuesday': read_string(store_info['Apn_neste_tirsdag']),
        'wednesday': read_string(store_info['Apn_neste_onsdag']),
        'thursday': read_string(store_info['Apn_neste_torsdag']),
        'friday': read_string(store_info['Apn_neste_fredag']),
        'saturday': read_string(store_info['Apn_neste_lordag']),
    }

    return {
        'name': read_string(store_info['Butikknavn']),

        'address': read_string(store_info['Gateadresse']),
        'zip_code': read_string(store_info['Gate_postnummer']),
        'postal': read_string(store_info['Gate_poststed']).title(),

        'category': read_store_category(store_info['Kategori']),

        'latitude': read_float(store_info['GPS_breddegrad']),
        'longitude': read_float(store_info['GPS_lengdegrad']),

        'opening_times': opening_times,
        'opening_times_next': opening_times_next,
    }


@transaction.atomic
def update_stores():
    """
    Fetch remote store database from vinmonopolet.no. Parse the data and update local database.
    """
    logging.info('Starting store database update')

    with urllib.request.urlopen(
            # FIXME: Change back when redirect is in place. http://www.vinmonopolet.no/api/butikker
            'https://www.vinmonopolet.no/medias/sys_master/locations/locations/h3c/h4a/8834253946910.csv'
    ) as f:
        f = f.read().decode('iso-8859-1').split('\r\n')

        logging.info('Remote database read. Updating local database.')

        reader = list(csv.DictReader(f[1:], delimiter=';', fieldnames=f[0].split(';')))

        # Used for logging progress
        number_of_items = len(reader)
        logging_interval = math.ceil(number_of_items / 100)
        i = 0

        for store_info in reader:
            store_info = store_info_to_store(store_info)

            try:
                store = Store.objects.get(name=store_info['name'])

                for key, value in store_info.items():
                    setattr(store, key, value)

                store.save()
            except Store.DoesNotExist:
                Store.objects.create(**store_info)

            i += 1

            if i % logging_interval == 0:
                logging.info('%.2f%% complete' % int(i / number_of_items * 100))

        logging.info('Database update complete')


if __name__ == '__main__':
    update_stores()
