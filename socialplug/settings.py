"""
Django settings for socialplug project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import django
from django.core.urlresolvers import reverse_lazy

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

try:
    from local_settings import *
except ImportError:
    pass

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'django.contrib.sites',
    # # auth collection
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.instagram',
    'allauth.socialaccount.providers.spotify',
    'feed',
    'main',
    # extensions?
    'django_extensions',
    'webpack_loader',
    'rest_framework',
    'rest_framework.authtoken',
]

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
)

ROOT_URLCONF = 'socialplug.urls'

WSGI_APPLICATION = 'socialplug.wsgi.application'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
                'django.contrib.auth.context_processors.auth',
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",

                # `allauth` needs this from django
                'django.template.context_processors.request',
            ],
            'debug': DEBUG,
            # 'loaders': [
            #     'django_jinja.loaders.AppLoader',
            #     'django_jinja.loaders.FileSystemLoader',
            # ]
        },
    },
]

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

SITE_ID = 1

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework_filters.backends.DjangoFilterBackend',
    ), 'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'api.pagination.TenItemsSetPagination'
}

SOCIALACCOUNT_QUERY_EMAIL = True
# social login scopes
SOCIALACCOUNT_PROVIDERS = \
    {
        'facebook':
            {
                'METHOD': 'js_sdk',
                'SCOPE': ['email', 'public_profile', 'user_likes',
                          'user_actions.books',
                          'user_actions.music'],
                'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
                'FIELDS': [
                    'id',
                    'email',
                    'first_name',
                    'last_name',
                    'verified',
                    'link',
                    'gender',
                    'picture',
                    'likes.limit(500){name,category,photos.limit(3){source}}',
                    'books{name,category,photos.limit(3){source}}',
                    'sports',
                    'music{photos.limit(3){source},name,category}',
                ],
                'EXCHANGE_TOKEN': True,
                'VERSION': 'v2.4'
            },

        'google':
            {'SCOPE': ['https://www.googleapis.com/auth/userinfo.profile',
                       'https://www.googleapis.com/auth/userinfo.email',
                       'https://www.googleapis.com/auth/youtube.readonly']
                , 'AUTH_PARAMS': {}},
        'instagram':
            {'SCOPE': ['basic']
                , 'AUTH_PARAMS': {}},
        'spotify':
            {'SCOPE': ['user-library-read', 'user-read-email']
                , 'AUTH_PARAMS': {}},

    }

AUTH_PROFILE_MODULE = 'main.UserProfile'
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
ACCOUNT_EMAIL_REQUIRED = True

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = ''

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, *MEDIA_URL.strip('/').split('/'))
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/'
ACCOUNT_USERNAME_MIN_LENGTH = 2
ACCOUNT_PASSWORD_MIN_LENGTH = 6
SOCIALACCOUNT_AUTO_SIGNUP = True
# SOCIALACCOUNT_ADAPTER = 'main.adapter.MySocialAccountAdapter'


WEBPACK_LOADER = {
    'DEFAULT': {
        'CACHE': DEBUG,
        'BUNDLE_DIR_NAME': 'dist/',  # must end with slash
        'STATS_FILE': os.path.join(BASE_DIR, 'webpack-stats.json'),
        'POLL_INTERVAL': 0.1,
        'IGNORE': ['.+\.hot-update.js', '.+\.map']
    }
}
django.setup()
