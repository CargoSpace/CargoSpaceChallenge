from __future__ import absolute_import, unicode_literals
# ^^^ The above is required if you want to import from the celery
# library.  If you don't have this then `from celery.schedules import`
# becomes `proj.celery.schedules` in Python 2.x since it allows
# for relative imports by default.
import os
gettext = lambda s: s
DATA_DIR = os.path.dirname(os.path.dirname(__file__))
"""
Django settings for csc project.

Generated by 'django-admin startproject' using Django 1.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# CELERY_BROKER_URL = 'amqp://myuser:mypassword@localhost:5672/dretnan-csc-4280924'
CELERY_BROKER_URL = 'redis://localhost:6379/0' # redis://:password@hostname:port/db_number
CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600, 'fanout_patterns': True}  # 1 hour.

#: Only add pickle to this list if your broker is secured
#: from unwanted access (see userguide/security.html)
CELERY_ACCEPT_CONTENT = ['json']
# CELERY_RESULT_BACKEND = 'db+sqlite:///results.sqlite'
CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_BACKEND = 'django-db'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
# CELERY_RESULT_BACKEND = 'django-cache'


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '4en8gryp2_)&z@-7uq91r8jf(46&oln60pal5f3l0!7#$l1n5n'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    '*',
]


# Application definition





ROOT_URLCONF = 'csc.urls'



WSGI_APPLICATION = 'csc.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases




# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Lagos'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

if DEBUG:
    STATIC_URL = '/static/'
    MEDIA_URL = '/media/'
    STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static_cdn")
    MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "media_cdn")
else:
    STATIC_URL = '/static/'
    MEDIA_URL = '/media/'
    STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static")
    MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "media")

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'csc', 'static'),
)
SITE_ID = 1


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'csc', 'templates'),],
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.core.context_processors.i18n',
                'django.core.context_processors.debug',
                'django.core.context_processors.request',
                'django.core.context_processors.media',
                'django.core.context_processors.csrf',
                'django.core.context_processors.tz',
                'sekizai.context_processors.sekizai',
                'django.core.context_processors.static',
                'cms.context_processors.cms_settings',
                'django.template.context_processors.request',
                'context_preprocessors.extra_context',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
                'django.template.loaders.eggs.Loader'
            ],
        },
    },
]


MIDDLEWARE_CLASSES = (
    'cms.middleware.utils.ApphookReloadMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware'
)

INSTALLED_APPS = (
    'rest_framework',
    'app',
    'dashboard',
    'contest',
    'rpc',
    'modernrpc',
    'djangocms_admin_style',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'cms',
    'menus',
    'sekizai',
    'treebeard',
    'djangocms_text_ckeditor',
    'filer',
    'easy_thumbnails',
    'djangocms_column',
    'djangocms_link',
    'cmsplugin_filer_file',
    'cmsplugin_filer_folder',
    'cmsplugin_filer_image',
    'cmsplugin_filer_utils',
    'djangocms_style',
    'djangocms_snippet',
    'djangocms_googlemap',
    'djangocms_video',
    'mptt',
    'pages',
    'taggit',

    'allauth',
    'allauth.account',
    #'allauth.socialaccount',
    ## include the providers you want to enable:
    #'allauth.socialaccount.providers.facebook',
    #'allauth.socialaccount.providers.twitter',
    #'allauth.socialaccount.providers.instagram',
    #'allauth.socialaccount.providers.google',
    'csc',
    'templatetag_handlebars',
    'django_celery_beat',
    'django_celery_results',
    'invitations',
)

MODERNRPC_METHODS_MODULES = [
    'rpc.rpc_methods'
]

# LANGUAGES = (
#     ## Customize this
#     ('en', gettext('en')),
# )

CMS_LANGUAGES = {
    ## Customize this
    1: [
        {
            'name': gettext('en'),
            'redirect_on_fallback': True,
            'hide_untranslated': False,
            'public': True,
            'code': 'en',
        },
    ],
    'default': {
        'redirect_on_fallback': True,
        'hide_untranslated': False,
        'public': True,
    },
}

CMS_TEMPLATES = (
    ## Customize this
    ('fullwidth.html', 'Fullwidth'),
    ('sidebar_left.html', 'Sidebar Left'),
    ('sidebar_right.html', 'Sidebar Right')
)

CMS_PERMISSION = True

CMS_PLACEHOLDER_CONF = {}

DATABASES = {
    'default': {
        'CONN_MAX_AGE': 0,
        'ENGINE': 'django.db.backends.sqlite3',
        'HOST': 'localhost',
        'NAME': 'project.db',
        'PASSWORD': '',
        'PORT': '',
        'USER': ''
    }
}

MIGRATION_MODULES = {
    
}

THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters'
)

META_SITE_PROTOCOL = 'http'
META_USE_SITES = True

PARLER_LANGUAGES = {
    1: (
        {'code': 'en',},
    ),
    'default': {
        'fallbacks': ['en'],
    }
}

PAGE_DEFAULT_TEMPLATE = 'pages/index.html'

PAGE_TEMPLATES = (
    ('pages/nice.html', 'nice one'),
    ('pages/cool.html', 'cool one'),
)

# This is defined here as a do-nothing function because we can't import
# django.utils.translation -- that module depends on the settings.
gettext_noop = lambda s: s

# here is all the languages supported by the CMS
PAGE_LANGUAGES = (
    ('en-us', gettext_noop('US English')),
)

# copy PAGE_LANGUAGES
languages = list(PAGE_LANGUAGES)

LANGUAGES = languages

TEMPLATE_CONTEXT_PROCESSORS = (
    'pages.context_processors.media',
    'django.core.context_processors.request',
    'csc.context_preprocessors.extra_context',
)

PAGE_USE_SITE_ID = True

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)


AUTH_PROFILE_MODULE = "account.UserProfile"