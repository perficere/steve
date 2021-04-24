from django.conf import settings

from binance.client import Client
from binance.exceptions import BinanceAPIException as APIException

from utils.metaclasses import Singleton


class Interface(metaclass=Singleton):
    def __init__(self):
        self.client = Client(settings.BINANCE_API_KEY, settings.BINANCE_API_SECRET)

    @property
    def healthy(self):
        try:
            response = self.client.get_system_status()
        except APIException:
            return False

        return response["status"] == 0
