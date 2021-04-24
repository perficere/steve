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


###########
# SECRETS #
###########

SECRET_KEY = "X.:IU=jrQLF+<uOBeh/ZK3vE4AaCL{.d;UO(g]>qV-w6sb:nfF"
INTERNAL_KEY = "bO|Q)[c)J[m|d]d{:+{vh:vkI7k6=*4M(^l$t9L-OG]d4jEla|"

BINANCE_API_KEY = "kClOWwtWDSCGVXfX4QtDxCUzKQoF2wLaZHJtIlmsMIzmI0IjxPoc9wrB6fUjvXtV"
BINANCE_API_SECRET = "1tifqLsFI2fnHw8Q8RW2fNmMgpYSqiLNcdaGVtXDKaw5YoHgdwT4gfxXsnWSyYQM"

BUDA_API_KEY = "DxCfsx1Fk8dTjPJ9OdjAH2j8e2FjqJ5Y"
BUDA_API_SECRET = "qx7qa2AulIvf17TIQKwM8qDdrxiurfziCIhDf24A"
