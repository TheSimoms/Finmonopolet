import os
import sys
import django
import logging
import math
import datetime

from django.db import transaction


sys.path.append(os.path.abspath(os.path.join('/'.join(__file__.split('/')[:-1]), os.pardir)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finmonopolet.settings')

django.setup()


from finmonopolet.update_database import read_csv_from_url, read_string, read_float, read_integer, read_store_category

from store.models import Store


def read_opening_times_week(week_number):
    if week_number is None:
        week_number = -1

    return week_number


def read_opening_times_hours(opening_hours):
    if opening_hours is None:
        opening_hours = 'Stengt'

    return opening_hours


def store_info_to_store(store_info):
    opening_times = {
        'week_number': read_opening_times_week(
            read_integer(store_info['Ukenummer'], True)),

        'monday': read_opening_times_hours(
            read_string(store_info['Apn_mandag'], True)),
        'tuesday': read_opening_times_hours(
            read_string(store_info['Apn_tirsdag'], True)),
        'wednesday': read_opening_times_hours(
            read_string(store_info['Apn_onsdag'], True)),
        'thursday': read_opening_times_hours(
            read_string(store_info['Apn_torsdag'], True)),
        'friday': read_opening_times_hours(
            read_string(store_info['Apn_fredag'], True)),
        'saturday': read_opening_times_hours(
            read_string(store_info['Apn_lordag'], True)),
    }
    opening_times_next = {
        'week_number': read_opening_times_week(
            read_integer(store_info['Ukenummer_neste'], True)),

        'monday': read_opening_times_hours(
            read_string(store_info['Apn_neste_mandag'], True)),
        'tuesday': read_opening_times_hours(
            read_string(store_info['Apn_neste_tirsdag'], True)),
        'wednesday': read_opening_times_hours(
            read_string(store_info['Apn_neste_onsdag'], True)),
        'thursday': read_opening_times_hours(
            read_string(store_info['Apn_neste_torsdag'], True)),
        'friday': read_opening_times_hours(
            read_string(store_info['Apn_neste_fredag'], True)),
        'saturday': read_opening_times_hours(
            read_string(store_info['Apn_neste_lordag'], True)),
    }

    # Correct for missing week numbers
    if opening_times['week_number'] == -1 or opening_times_next['week_number'] == -1:
        if opening_times['week_number'] == -1 and opening_times_next['week_number'] != -1:
            opening_times['week_number'] = opening_times_next['week_number'] - 1
        elif opening_times['week_number'] != -1 and opening_times_next['week_number'] == -1:
            opening_times_next['week_number'] = opening_times['week_number'] + 1
        else:
            opening_times['week_number'] = current_week_number
            opening_times_next['week_number'] = current_week_number + 1

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

    reader = read_csv_from_url(
        # FIXME: Change back when redirect is in place. http://www.vinmonopolet.no/api/butikker
        'https://www.vinmonopolet.no/medias/sys_master/locations/locations/h3c/h4a/8834253946910.csv'
    )

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
    current_week_number = datetime.datetime.utcnow().isocalendar()[1]

    update_stores()
