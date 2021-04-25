from django.conf import settings

from trading_api_wrappers.Buda import Auth as Client
from trading_api_wrappers.buda.OrderPriceType import LIMIT, MARKET  # noqa: F401
from trading_api_wrappers.buda.OrderType import ASK, BID
from trading_api_wrappers.errors import APIException

from utils.metaclasses import Singleton

from .base import BaseInterface


class Interface(BaseInterface, metaclass=Singleton):
    def __init__(self):
        self.client = Client(
            settings.BUDA_API_KEY, settings.BUDA_API_SECRET, return_json=True
        )

    ##########
    # PUBLIC #
    ##########

    @property
    def is_healthy(self):
        try:
            response = self.client.markets()
        except APIException:
            return False

        return bool(response)

    def get_orderbook(self, base, quote):
        orderbook = self.client.order_book(market_id=f"{base}-{quote}")["order_book"]

        orderbook[BID] = orderbook.pop("bids")
        orderbook[ASK] = orderbook.pop("asks")

        return orderbook

    #################
    # AUTHENTICATED #
    #################

    def get_available_balance(self, ticker):
        return self.client.balance(currency=ticker)["balance"]["available_amount"][0]

    def place_order(self, base, quote, side, type_, amount, price):
        self.client.new_order(
            market_id=f"{base}-{quote}",
            order_type=side,
            price_type=type_,
            amount=amount,
            price=price,
        )
