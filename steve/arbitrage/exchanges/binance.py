from django.conf import settings

from binance.client import Client

from utils.metaclasses import Singleton


class Interface(metaclass=Singleton):
    def __init__(self):
        self.client = Client(settings.BINANCE_API_KEY, settings.BINANCE_API_SECRET)
