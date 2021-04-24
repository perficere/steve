from keys import BINANCE
from binance.client import Client
from exchange import Exchange
import settings


class Binance(Exchange):

    def __init__(self):
        Exchange.__init__(self, "binance", BINANCE['key'], BINANCE['secret'])
        self.client = Client(self.key, self.secret)

    def get_balances(self):
        balances = {}
        for ticker in settings.TICKERS:
            balances[ticker] = float(self.client.get_asset_balance(asset=ticker)['free'])
        return balances

    def get_order_book(self, ticker, n=None):
        depth = self.client.get_order_book(symbol=ticker)
        order_book = {}
        order_book['bids'] = depth['bids'][:n]
        order_book['asks'] = depth['asks'][:n]

        for order_type in order_book:
            formatted_values = []
            for order in order_book[order_type]:
                formatted_values.append([float(x) for x in order])
            order_book[order_type] = formatted_values
        return {'bids': [[0.004884, 8.8]], 'asks': [[0.004886, 15.94]]}
        return order_book

    def get_ticker(self, ticker='BNBBTC'):
        res = self.client.get_avg_price(symbol=ticker)
        return res

    def make_buy_order(self, ticker, price, size):
        print('Placing Buy order in Binance')
        order = self.client.order_limit_buy(
            symbol=ticker,
            quantity=size,
            price=str(round(price * 1.001, 6)))
        print(order)
        print(f"Order placed with id {order['orderId']}")
        # print(client.get_open_orders(symbol=ticker))

    def make_sell_order(self, ticker, price, size):
        print('Placing sell order in Binance')
        order = self.client.order_limit_sell(
            symbol=ticker,
            quantity=size,
            price=str(round(price * 0.999, 6)))
        print(order)
        print(f"Order placed with id {order['orderId']}")
        # print(client.get_open_orders(symbol=ticker))
