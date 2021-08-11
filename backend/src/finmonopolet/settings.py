import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Security settings

SECRET_KEY = os.environ['SECRET_KEY']

DEBUG = os.getenv('DEBUG', default='False') in ['True', '1']

_HTTP_HOST = os.environ['HTTP_HOST']
_HTTP_PORT = os.environ['HTTP_PORT']

ALLOWED_HOSTS = [
    _HTTP_HOST,
    'localhost',
    '127.0.0.1',
]

CORS_ORIGIN_WHITELIST = [
    'http://{}{}'.format(
        _HTTP_HOST,
        '' if _HTTP_PORT == '80' else ':{}'.format(_HTTP_PORT)
    ),
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.contenttypes',

    'corsheaders',
    'django_extensions',
    'rest_framework',

    'products',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'finmonopolet.urls'

TEMPLATES = []

WSGI_APPLICATION = 'finmonopolet.wsgi.application'


# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.environ['DB_HOST'],
        'PORT': os.getenv('DB_PORT', '5432'),
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASSWORD'],
    }
}


# Internationalization

LANGUAGE_CODE = 'nb-no'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Django REST Framework

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'DEFAULT_PERMISSION_CLASSES': [],
    'UNAUTHENTICATED_USER': None,
    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework.filters.OrderingFilter',
        'rest_framework.filters.SearchFilter',
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 12
}
