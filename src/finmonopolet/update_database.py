from store.models import StoreCategory


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
