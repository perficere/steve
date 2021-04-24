import settings


class Exchange:

    def __init__(self, name, key, secret):
        self.name = name
        self.key = key
        self.secret = secret
        self._balances = {}
        print(f"Exchange created: {self.name}")

    # In the meantime, later we will maybe use db
    @property
    def balances(self):
        return {'BTC': 1, "ETH": 1, "LTC": 1}

    def get_trading_pair(self, tickers):
        return settings.TRADING_PAIRS[self.name][tickers[0]] + settings.TRADING_PAIRS[self.name]['DIV'] + settings.TRADING_PAIRS[self.name][tickers[1]]

    def __repr__(self):
        return self.name
