from django.conf import settings

BID, ASK = range(2)


class BaseInterface:
    def __init__(self):
        raise NotImplementedError()

    ##########
    # PUBLIC #
    ##########

    @property
    def is_healthy(self):
        raise NotImplementedError()

    def get_orderbook(self, base, quote):
        raise NotImplementedError()

    def get_market(self, base, quote):
        orderbook = self.get_orderbook(base, quote)

        return {
            BID: orderbook[BID][0],
            ASK: orderbook[ASK][0],
        }

    #################
    # AUTHENTICATED #
    #################

    def get_available_balance(self, ticker):
        raise NotImplementedError()

    def place_order(self, base, quote, side, type, amount, price):
        raise NotImplementedError()

    def get_all_available_balances(self):
        return {ticker: self.get_available_balance(ticker) for ticker in settings.TICKERS}
