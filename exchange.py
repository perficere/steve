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

    def check_order_status(self, order_id, trading_pair):
        details = self.get_order_details(order_id, trading_pair)
        if details['status'] in ['FILLED', 'traded']:
            # order completed succesfully, register en db
            return True
        else:
            # Handle incomplete order
            return False

    def get_trading_pair(self, tickers):
        return settings.TRADING_PAIRS[self.name][tickers[0]] + settings.TRADING_PAIRS[self.name]['DIV'] + settings.TRADING_PAIRS[self.name][tickers[1]]

    def __repr__(self):
        return self.name
