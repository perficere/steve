from django.conf import settings

from binance import enums
from binance.client import Client
from binance.exceptions import BinanceAPIException as APIException

from utils.metaclasses import Singleton

from .base import ASK, BID, BaseInterface


class Interface(BaseInterface, metaclass=Singleton):
    BUY = enums.SIDE_BUY
    SELL = enums.SIDE_SELL

    LIMIT = enums.ORDER_TYPE_LIMIT
    MARKET = enums.ORDER_TYPE_MARKET

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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

    def place_limit_order(self, base, quote, side, amount, price):
        self.client.create_order(
            symbol=f"{base}{quote}",
            side={BID: self.BUY, ASK: self.SELL}[side],
            type=self.LIMIT,
            quantity=amount,
            price=price,
        )

    def get_order_details(self, order_id, trading_pair):
        status = self.client.get_order(
            symbol=trading_pair,
            orderId=order_id)
        details = {
            "market": status["symbol"],
            "id": status["orderId"],
            "status": status["status"],
            "side": status["side"],
            "price": status["price"],
            "size": status["executedQty"],
            "cost": float(status["price"]) * float(status["executedQty"])
        }
        return details
    def place_market_order(self, base, quote, side, amount):
        self.client.create_order(
            symbol=f"{base}{quote}",
            side={BID: self.BUY, ASK: self.SELL}[side],
            type=self.MARKET,
            quantity=amount,
        )
