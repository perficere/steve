from django.conf import settings

from binance.client import Client
from binance.enums import ORDER_TYPE_LIMIT as LIMIT  # noqa: F401
from binance.enums import ORDER_TYPE_MARKET as MARKET  # noqa: F401
from binance.enums import SIDE_BUY as BUY  # noqa: F401
from binance.enums import SIDE_SELL as SELL  # noqa: F401
from binance.exceptions import BinanceAPIException as APIException

from utils.metaclasses import Singleton

from .base import ASK, BID, BaseInterface


class Interface(BaseInterface, metaclass=Singleton):
    def __init__(self):
        self.client = Client(settings.BINANCE_API_KEY, settings.BINANCE_API_SECRET)

    ##########
    # PUBLIC #
    ##########

    @property
    def is_healthy(self):
        try:
            response = self.client.get_system_status()
        except APIException:
            return False

        return response["status"] == 0

    def get_orderbook(self, base, quote):
        orderbook = self.client.get_order_book(symbol=f"{base}{quote}")

        orderbook[BID] = orderbook.pop("bids")
        orderbook[ASK] = orderbook.pop("asks")

        return orderbook

    #################
    # AUTHENTICATED #
    #################

    def get_available_balance(self, ticker):
        return self.client.get_asset_balance(asset=ticker)["free"]

    def place_order(self, base, quote, side, type_, amount, price):
        self.client.create_order(
            symbol=f"{base}{quote}",
            side=side,
            type=type_,
            quantity=amount,
            price=price,
        )
