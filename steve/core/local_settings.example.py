from decimal import Decimal

from .settings import *  # noqa: F401,F403

#############
# DATABASES #
#############

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": "postgres",
        "PASSWORD": "password",
        "HOST": "db",
        "PORT": 5432,
    }
}


#########
# EMAIL #
#########

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_PASSWORD = "password"
EMAIL_HOST_USER = "example@gmail.com"
EMAIL_PORT = 25
EMAIL_USE_TLS = False
EMAIL_USE_SSL = False


###############
# ENVIRONMENT #
###############

DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]


##############
# PARAMETERS #
##############

TICKERS = ["BTC", "ETH", "LTC"]
MARKETS = (["ETH", "BTC"],)

MIN_DELTA = Decimal("0.015")

MIN_SIZE = {"ETHBTC": Decimal("0.001"), "LTCBTC": Decimal("0.01")}  # Defined by Binance
MAX_SIZE = {"ETHBTC": Decimal("0.03"), "LTCBTC": Decimal("0.1")}
STEP_SIZE = {"ETHBTC": "0.001", "LTCBTC": "0.01"}


FEES = Decimal("0.007")

LOOP_N = 200

###########
# SECRETS #
###########

SECRET_KEY = "X.:IU=jrQLF+<uOBeh/ZK3vE4AaCL{.d;UO(g]>qV-w6sb:nfF"
INTERNAL_KEY = "bO|Q)[c)J[m|d]d{:+{vh:vkI7k6=*4M(^l$t9L-OG]d4jEla|"

BINANCE_API_KEY = "example"
BINANCE_API_SECRET = "example"

BUDA_API_KEY = "example"
BUDA_API_SECRET = "example"

TELEGRAM_TOKEN = "6381479124:WgiZ7xCC5EWQ_GncQe0vwvB71-0CXuDXods"
TELEGRAM_CHAT_ID = -583560951
