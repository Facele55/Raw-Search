import os
from dotenv import load_dotenv
from django.utils.translation import gettext_lazy as _
from pathlib import Path

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'django.contrib.humanize',

    'admin_honeypot',
    'dbbackup',  # django-dbbackup
    'dbbackup_ui',
    'smuggler',
    'django_filters',
    'django_elasticsearch_dsl',

    'core.apps.CoreConfig',
    'analytics.apps.AnalyticsConfig',
    'users.apps.UsersConfig',
    'feedback.apps.FeedbackConfig',
    'backups.apps.BackupsConfig',
    'crawler.apps.CrawlerConfig',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'users.LoginCheckMiddleWare.LoginCheckMiddleWare',

]

ROOT_URLCONF = 'rawsearch.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'rawsearch.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases


DATABASES = {
    'default': {},
    # for users, admins and other dependencies
    'users_db': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'raw_users_db.sqlite3'),
    },
    # for feedback
    'feedback_db': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'raw_feedbacks_db.sqlite3'),
    },
    # for analytics
    'analytics_db': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('ANALYTICS_DB_NAME'),
        'USER': os.getenv('ANALYTICS_DB_USER'),
        'PASSWORD': os.getenv('ANALYTICS_DB_PASSWORD'),
        'HOST': os.getenv('ANALYTICS_DB_HOST'),
        'PORT': os.getenv('ANALYTICS_DB_PORT'),
    },
    # for core
    'search_db': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('SEARCH_DB_NAME'),
        'USER': os.getenv('SEARCH_DB_USER'),
        'PASSWORD': os.getenv('SEARCH_DB_PASSWORD'),
        'HOST': os.getenv('SEARCH_DB_HOST'),
        'PORT': os.getenv('SEARCH_DB_PORT'),
        'TEST': {'DEPENDENCIES': [], },
    },
    # for crawler
    'crawler_db': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('CRAWLER_DB_NAME'),
        'USER': os.getenv('CRAWLER_DB_USER'),
        'PASSWORD': os.getenv('CRAWLER_DB_PASSWORD'),
        'HOST': os.getenv('CRAWLER_DB_HOST'),
        'PORT': os.getenv('CRAWLER_DB_PORT'),
    },
}

DATABASE_ROUTERS = ['rawsearch.router.AuthRouter', 'rawsearch.router.CheckerRouter']

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en'

LANGUAGES = [
    ('en', _('English')),
    ('pl', _('Polish')),
    ('uk', _('Ukrainian'))

]
LOCALE_PATHS = [os.path.join(BASE_DIR, 'dir/locale', )]


TIME_ZONE = 'Europe/Warsaw'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

"""
STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static/static')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static/static'),
]
"""

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# For Custom USER
AUTH_USER_MODEL = "users.CustomUser"

# Registering Custom Backend "EmailBackEnd"
# AUTHENTICATION_BACKENDS = ['users.EmailBackEnd.EmailBackEnd']

session_expire_at_browser_close = True

DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
DBBACKUP_STORAGE_OPTIONS = {'location': os.path.join(BASE_DIR, 'dir/backup/')}


# Uncomment ONLY IF U HAVE SSL CERTIFICATE
# SECURE_SSL_REDIRECT = True
CSRF_COOKIE_SECURE = False
CSRF_COOKIE_SAMESITE = 'Strict'
SESSION_COOKIE_SECURE = False
SECURE_BROWSER_XSS_FILTER = False
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 300  # set low, but when site is ready for deployment, set to at least 15768000 (6 months)
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'loggers': {
        'django': {
            'handlers': ['info', 'debug', 'warning', 'critic'],
            'level': 'DEBUG'
        }
    },
    'handlers': {
        'info': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'dir/logs/info/info.log'),
            'formatter': 'simpleRe',
            'backupCount': 100,  # keep at most 10 log files
            'maxBytes': 5*1024*1024,  # 5242880,  # 5*1024*1024 bytes (5MB)
        },
        'debug': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'dir/logs/debug/debug.log'),
            'backupCount': 100,  # keep at most 10 log files
            'maxBytes': 5242880,  # 5*1024*1024 bytes (5MB)
            'formatter': 'simpleRe',
        },

        'warning': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'dir/logs/warning/warning.log'),
            'backupCount': 100,  # keep at most 10 log files
            'maxBytes': 5242880,  # 5*1024*1024 bytes (5MB)
            'formatter': 'simpleRe',
        },
        'critic': {
            'level': 'CRITICAL',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'dir/logs/critic/critic.log'),
            'backupCount': 100,  # keep at most 10 log files
            'maxBytes': 5242880,  # 5*1024*1024 bytes (5MB)
            'formatter': 'simpleRe',
        }
    },
    'formatters': {
        'simpleRe': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message} ',
            'style': '{',
        }

    }
}
ELASTICSEARCH_DSL = {
    'default': {
        'hosts': 'localhost:9200',  # '0.0.0.0:9200'
        # 'hosts': os.getenv('ES_PORT'),  # '0.0.0.0:9200'
    },
}

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
}
