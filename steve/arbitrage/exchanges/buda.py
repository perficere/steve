from django.conf import settings

from trading_api_wrappers import Buda as Client

from utils.metaclasses import Singleton


class Interface(metaclass=Singleton):
    def __init__(self):
        self.client = Client.Auth(settings.BUDA_API_KEY, settings.BUDA_API_SECRET)
