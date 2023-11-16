from django.conf import settings

from ..models import OrderSide


def cached(func):
    def wrapper(interface):
        if func.__name__ not in interface._cache:
            interface._cache[func.__name__] = func(interface)

        return interface._cache[func.__name__]

    return wrapper


class BaseInterface:
    def __init__(self):
        self.clear_cache()

    def clear_cache(self):
        self._cache = {}

    ##########
    # PUBLIC #
    ##########

    @property
    def is_healthy(self):
        raise NotImplementedError()

    def get_orderbook(self, base, quote):
        raise NotImplementedError()

    @property
    @cached
    def orderbooks(self):
        return {tuple(market): self.get_orderbook(*market) for market in settings.MARKETS}

    @property
    @cached
    def prices(self):
        return {
            tuple(market): {
                OrderSide.BID: orderbook[OrderSide.BID][0],
                OrderSide.ASK: orderbook[OrderSide.ASK][0],
            }
            for (market, orderbook) in self.orderbooks.items()
        }

    #################
    # AUTHENTICATED #
    #################

    def get_available_balance(self, ticker):
        raise NotImplementedError()

    def place_limit_order(self, base, quote, side, type_, amount, price):
        raise NotImplementedError()

    def place_market_order(self, base, quote, side, type_, amount):
        raise NotImplementedError()

    @property
    @cached
    def available_balances(self):
        return {ticker: self.get_available_balance(ticker) for ticker in settings.TICKERS}
