from django.conf import settings

from trading_api_wrappers import Buda as Client
from trading_api_wrappers.errors import APIException

from utils.metaclasses import Singleton


class Interface(metaclass=Singleton):
    def __init__(self):
        self.client = Client.Auth(settings.BUDA_API_KEY, settings.BUDA_API_SECRET)

    @property
    def healthy(self):
        try:
            response = self.client.markets()
        except APIException:
            return False

        return bool(response)
