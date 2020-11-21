import os
from pathlib import Path
from corsheaders.defaults import default_headers
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-f^&musa-5v7vhcgp!9yg06!*ehi(19rf*9pdf$*w-m2s)hgge'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["localhost",
                 "127.0.0.1",
                 "192.168.100.4"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # third party
    'rest_framework',
    'corsheaders',
    'rest_framework_simplejwt.token_blacklist',
    'rest_registration',
    'django.chatbot',
    'import_export',
    "rest_framework_tracking",

    # My Apps
    'facebook',
    'google',
    'account',
    'permission',
    'chat',
    'posts',
    'contacts'
]
FACEBOOK_APP_ID = "3684441794901564"
FACEBOOK_APP_SECRET = "8459910c29c0b0b2bdbeede63af135cd"

AUTH_USER_MODEL = 'account.User'

START_MESSAGE = "Welcome to ChatBotAI"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


CORS_ORIGIN_WHITELIST = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://192.168.100.4:8000",
    "http://192.168.100.4:8080",
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",
    "http://localhost:3000",
    "http://127.0.0.1:8080",
    "http://127.0.0.1:3000",
    "http://192.168.100.4:8000",
    "http://192.168.100.4:8080",
]

CSRF_TRUSTED_ORIGINS = [
    "localhost",
    "127.0.0.1",
    "192.168.100.4"
]
CORS_ALLOW_HEADERS = list(default_headers) + [
    'contenttype',
]

ROOT_URLCONF = 'app.urls'

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

WSGI_APPLICATION = 'app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'wemeet_db',
        'USER': 'postgres',
        'PASSWORD': 'zaihtunlu',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

# Base url to serve media files
MEDIA_URL = '/media/'

# Path where media is stored
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=6*30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7*30),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(days=5*30),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=6*30),
}


REST_REGISTRATION = {
    'REGISTER_VERIFICATION_URL': 'http://localhost:8080/verify-user/',
    'RESET_PASSWORD_VERIFICATION_URL': 'http://localhost:8080/reset-password/',
    'REGISTER_EMAIL_VERIFICATION_URL': 'http://localhost:8080/verify-email/',
    'REGISTER_VERIFICATION_ENABLED': False,
    'VERIFICATION_FROM_EMAIL': 'saihtunlu14996@gmail.com',
    'USER_LOGIN_FIELDS': ['email'],
    'LOGIN_AUTHENTICATE_SESSION': 'timestamp',
    'REGISTER_VERIFICATION_EMAIL_TEMPLATES': {
        'subject':  'rest_registration/register/subject.txt',
        'text_body':  'rest_registration/register/body.txt',
        'html_body':  'rest_registration/register/body.html',
    },
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'saihtunlu14996@gmail.com'
EMAIL_HOST_PASSWORD = 'fmxjmbnlzlksldbk'  # past the key or password app here
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'default from email'
