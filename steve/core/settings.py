import os
import sys
from decimal import Decimal

import dj_database_url
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

# Build paths inside the project like this: os.path.join(BASE_DIR, ...).
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROJECT_NAME = "steve"


##########################
# APPLICATION DEFINITION #
##########################

THIRD_PARTY = [
    "rest_framework",
    "corsheaders",
    "whitenoise.runserver_nostatic",
    "django_extensions",
    "admin_numeric_filter",
]

FIRST_PARTY = [
    "accounts.apps.AccountsConfig",
    "arbitrage.apps.ArbitrageConfig",
]

BUILT_IN = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
]

INSTALLED_APPS = THIRD_PARTY + FIRST_PARTY + BUILT_IN


##################
# AUTHENTICATION #
##################

AUTH_USER_MODEL = "accounts.User"


#####################
# COMMON MIDDLEWARE #
#####################

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.common.BrokenLinkEmailsMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


########
# CORS #
########

CORS_ORIGIN_ALLOW_ALL = True


#############
# DATABASES #
#############

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DATABASE_NAME"),
        "USER": os.environ.get("DATABASE_USER"),
        "PASSWORD": os.environ.get("DATABASE_PASSWORD"),
        "HOST": os.environ.get("DATABASE_HOST"),
        "PORT": os.environ.get("DATABASE_PORT"),
    }
}

if "DATABASE_URL" in os.environ:
    DATABASES["default"] = dj_database_url.config(ssl_require=True)


#########
# EMAIL #
#########

ADMINS = [("Alex Apt", "aapt@uc.cl"), ("Ariel Martínez", "ariel@martinezs.cl")]
MANAGERS = ADMINS

EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_PORT = int(os.environ.get("EMAIL_HOST_PORT", "25"))
EMAIL_USE_TLS = bool(int(os.environ.get("EMAIL_USE_TLS", "0")))
EMAIL_USE_SSL = bool(int(os.environ.get("EMAIL_USE_SSL", "0")))

EMAIL_USE_LOCALTIME = True


###############
# ENVIRONMENT #
###############

TEST = "test" in sys.argv
DJANGO_ENV = os.environ.get("DJANGO_ENV")
DEBUG = DJANGO_ENV == "development"
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(" ")


##################
# HTML TEMPLATES #
##################

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "core", "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]


###########
# LOGGING #
###########

PROPAGATE_EXCEPTIONS = True
DEFAULT_LOGGING_LEVEL = "INFO" if DEBUG else "WARNING"
LOGGING_LEVEL = os.environ.get("LOGGING_LEVEL", DEFAULT_LOGGING_LEVEL)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
        "null": {
            "class": "logging.NullHandler",
        },
    },
    "loggers": {
        "django.security.DisallowedHost": {
            "handlers": ["null"],
            "level": "CRITICAL",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": LOGGING_LEVEL,
    },
}


##############
# PARAMETERS #
##############

ITERATIONS_PER_TRIGGER = int(os.environ.get("ITERATIONS_PER_TRIGGER", "1"))
SECONDS_BETWEEN_ITERATIONS = int(os.environ.get("ITERATIONS_PER_TRIGGER", "0"))

TICKERS = ["BTC", "ETH", "LTC"]
MARKETS = (["ETH", "BTC"],)

MIN_DELTA = Decimal(os.environ.get("MIN_DELTA", "inf"))

MIN_AMOUNTS = {
    "ETHBTC": Decimal("0.001"),
    "LTCBTC": Decimal("0.01"),
}
MAX_AMOUNTS = {
    "ETHBTC": Decimal("0.03"),
    "LTCBTC": Decimal("0.1"),
}
STEP_AMOUNTS = {"ETHBTC": Decimal("0.001"), "LTCBTC": Decimal("0.01")}


###########
# SECRETS #
###########

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")
INTERNAL_KEY = os.environ.get("INTERNAL_KEY")

BINANCE_API_KEY = os.environ.get("BINANCE_API_KEY")
BINANCE_API_SECRET = os.environ.get("BINANCE_API_SECRET")

BUDA_API_KEY = os.environ.get("BUDA_API_KEY")
BUDA_API_SECRET = os.environ.get("BUDA_API_SECRET")

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
TELEGRAM_CHAT_ID = None if (TELEGRAM_CHAT_ID is None) else int(TELEGRAM_CHAT_ID)


##########
# SENTRY #
##########

sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN", ""),
    integrations=[DjangoIntegration()],
    environment=DJANGO_ENV,
)


################
# STATIC FILES #
################

STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")


########
# URLS #
########

ROOT_URLCONF = "core.urls"
APPEND_SLASH = False


########
# WSGI #
########

WSGI_APPLICATION = "core.wsgi.application"
