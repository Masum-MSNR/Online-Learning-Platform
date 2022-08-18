import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-tzsoczy)u=c_1n3x@vvg(+l5k+&!mg8u)wdp^)@k(8z*#f51t^'

DEBUG = False


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'nam.bd88@gmail.com'
EMAIL_HOST_PASSWORD = 'dvprfbjsdwbcxsfl'

ALLOWED_HOSTS = [
    'online-learning-platform.azurewebsites.net',
    '127.0.0.1',
]
CSRF_TRUSTED_ORIGINS = [
    'https://*.online-learning-platform.azurewebsites.net',
    'https://*.127.0.0.1',
]

GOOGLE_DRIVE_STORAGE_JSON_KEY_FILE = 'base/cred.json'
# GOOGLE_DRIVE_STORAGE_MEDIA_ROOT = '<base google drive path for file uploads>'

AUTH_USER_MODEL = 'base.User'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'fontawesomefree',
    'base.apps.BaseConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'online_learning_platform.urls'

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
            'libraries':{
                'my_filters': 'base.my_filters',
            }
        },
    },
]

WSGI_APPLICATION = 'online_learning_platform.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'onlinelearning',
        'CLIENT': {
            'host': 'mongodb://localhost:27017',
            # 'username': 'masum',
            # 'password': 'masum'
        }
    }
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # }
}


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


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = 'base/static/'

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

if DEBUG:
    STATICFILES_DIRS = [os.path.join(BASE_DIR, STATIC_URL)]
else:
    STATIC_ROOT = os.path.join(BASE_DIR, 'static_files/')


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
