from django.conf import settings

from trading_api_wrappers.buda import BudaAuth as Client
from trading_api_wrappers.buda import constants
from trading_api_wrappers.errors import APIException

from utils.metaclasses import Singleton

from .base import ASK, BID, BaseInterface


class Interface(BaseInterface, metaclass=Singleton):
    __name__ = "Buda"

    BUY = constants.OrderType.BID
    SELL = constants.OrderType.ASK

    LIMIT = constants.OrderPriceType.LIMIT
    MARKET = constants.OrderPriceType.MARKET

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
        res = self.client.new_order(
            market_id=f"{base}-{quote}",
            order_type=side,
            price_type=type_,
            amount=amount,
            limit=price,
        )
        return res["order"]["id"]

    def place_limit_order(self, base, quote, side, amount, price):
        res = self.client.new_order(
            market_id=f"{base}{quote}",
            order_type={BID: self.BUY, ASK: self.SELL}[side],
            price_type=self.LIMIT,
            amount=amount,
            limit=price,
        )
        return res["order"]["id"]

    def place_market_order(self, base, quote, side, amount):
        res = self.client.new_order(
            market_id=f"{base}{quote}",
            order_type={BID: self.BUY, ASK: self.SELL}[side],
            price_type=self.MARKET,
            amount=amount,
        )
        return res["order"]["id"]

    def get_order_details(self, order_id, market=None):
        response = self.client.order_details(order_id=order_id)["order"]
        details = {
            "market": response["market_id"],
            "id": response["id"],
            "status": response["state"],
            "side": response["type"],
            "price": response["limit"][0],
            "amount": response["traded_amount"][0],
            "cost": response["total_exchanged"][0],
        }
        return details
