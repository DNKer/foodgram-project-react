""" FoodGram Community
Copyright (C) 2023 Authors: Dmitry Korepanov, Yandex practikum
License Free
Version: 1.0.1. 2023"""

import os

from dotenv import load_dotenv


load_dotenv()

DEFAULT_PAGE_SIZE: int = 6

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.getenv(
    'SECRET_KEY',
    default='secret_code_must_be_here'
)

DEBUG = os.getenv('DEBUG', default=False)

ALLOWED_HOSTS = [os.getenv(
    'ALLOWED_HOSTS').split()]

AUTH_USER_MODEL = 'users.User'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'api.apps.ApiConfig',
    'recipes.apps.RecipesConfig',
    'users.apps.UsersConfig',
    'corsheaders',
    'djoser',
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'foodgram.urls'
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'foodgram.wsgi.application'

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'sent_emails')
DEFAULT_FROM_EMAIL = 'noreply@food.ru'


if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': os.getenv('DB_ENGINE',
                                default='django.db.backends.postgresql'),
            'NAME': os.getenv('DB_NAME',
                              default='postgres'),
            'USER': os.getenv('POSTGRES_USER',
                              default='postgres'),
            'PASSWORD': os.getenv('POSTGRES_PASSWORD',
                                  default='postgres'),
            'HOST': os.getenv('DB_HOST',
                              default='db'),
            'PORT': os.getenv('DB_PORT',
                              default='5432')
        }
    }


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
            ('django.contrib.auth.password_validation.'
             'UserAttributeSimilarityValidator'),
    },
    {
        'NAME':
            'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
            'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
            'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'ru-Ru'

TIME_ZONE = 'Asia/Yekaterinburg'

USE_I18N = True

USE_L10N = True

USE_TZ = True

EMPTY = '-пусто-'


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
    ],
    'DEFAULT_PAGINATION_CLASS':
        'api.pagination.LimitOffsetPagination',
        'PAGE_SIZE': DEFAULT_PAGE_SIZE,
}

DJOSER = {
    'SERIALIZERS': {
        'user':
        'api.serializers.CustomUserSerializer',
        'user_create':
        'api.serializers.CustomUserCreateSerializer',
        'current_user':
        'api.serializers.CustomUserSerializer',
    },
    'PERMISSIONS': {
        'user':
        ['djoser.permissions.CurrentUserOrAdminOrReadOnly'],
        'user_list':
        ['rest_framework.permissions.AllowAny'],
    },
    'HIDE_USERS': False,
}
