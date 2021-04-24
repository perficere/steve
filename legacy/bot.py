import settings


class Bot:

    def __init__(self, exchanges: list):
        self.exchanges = exchanges
        print(f"Bot started with {len(self.exchanges)} exchanges")

    def get_balances(self):
        total_balances = {}
        for e in self.exchanges:
            balances = e.get_balances()
            if balances:
                for b in balances:
                    if b not in total_balances:
                        total_balances[b] = balances[b]
                    else:
                        total_balances[b] += balances[b]
            else:
                print(f"ALERT: Could not fetch balances from {e.name}")
        return total_balances

    @property
    def balances(self):
        return self.get_balances()

    def get_order_books(self, tickers, n=None):  # Get dict with 'asks' ands 'bids'
        order_books = {}
        for e in self.exchanges:
            trading_pair = e.get_trading_pair(tickers)
            res = e.get_order_book(trading_pair, n)
            order_books[e] = res

        # HARD CODED FOR TESTING
        # order_books = {'buda': {'bids': [[0.04, 2.0]], 'asks': [[0.042, 0.075]]}, 'binance': {'bids': [[0.043, 2.945]], 'asks': [[0.044, 0.004]]}}
        return order_books

    def check_if_trade_available(self, tickers):
        order_books = self.get_order_books(tickers, 1)
        # order_books = order_book = {'buda': {'bids': [[0.005057, 6.781e-05]], 'asks': [[0.0051, 2.26342815]]}, 'binance': {'bids': [[0.004884, 8.8]], 'asks': [[0.004886, 15.94]]}}
        best_asks, best_bids, delta = self.get_best_delta(order_books)
        if delta > settings.MIN_DELTA:
            asks_price, asks_size, asks_exchange = best_asks
            bids_price, bids_size, bids_exchange = best_bids

            asks_trading_pair = asks_exchange.get_trading_pair(tickers)
            bids_trading_pair = bids_exchange.get_trading_pair(tickers)

            # BIDS IS THE PRICE TO SELL AND ASKS THE PRICE TO BUY
            # SELL IN BIDS BUY IN ASKS
            print(f"{''.join(tickers)} TRADE FOUND WITH DELTA {round(delta * 100, 4)}%")
            size = min(asks_size, bids_size, settings.MAX_SIZE[tickers[0]])
            asks = self.create_order(asks_exchange, asks_trading_pair, asks_price, size)
            bids = self.create_order(bids_exchange, bids_trading_pair, bids_price, size)
            order = {'asks': asks, 'bids': bids}
            # self.paper_trade(order)
            self.trade(order)
        else:
            print(f'NO {"".join(tickers)} TRADE WITH ENOUGH DELTA FOUND {round(delta * 100, 4)}%')

    def get_best_delta(self, order_book):
        bids = []
        asks = []
        for exchange in order_book:
            for elem in order_book[exchange]['bids']:
                bids.append([*elem, exchange])
            for elem in order_book[exchange]['asks']:
                asks.append([*elem, exchange])
        best_bid = max(bids)
        best_ask = min(asks)
        delta = (best_bid[0] - best_ask[0]) / best_ask[0]
        return best_ask, best_bid, delta

    def create_order(self, exchange, trading_pair, price, size):
        return {'exchange': exchange, "trading_pair": trading_pair, "price": price, "size": size}

    def paper_trade(self, order=None):
        # ETH-BTC WITH DELTA1
        print(order)
        # order = {'asks':{'exchange':"buda", "price":0.04, "size":2}, 'bids':{'exchange':"binance", "price":0.045, "size":2}}
        pass
        for e in self.exchanges:
            if e.name == 'buda':
                buda = e
            else:
                binance = e

        print("\nSTARTING BALANCE: ")
        start_balances = self.balances
        print(self.balances)
        # BUY FROM BUDA (BUYING ETH)
        size = order['asks']['size']
        price = order['asks']['price']
        buda.balances = ['ETH', size]
        buda.balances = ['BTC', -size * price]

        print("\nHALF WAY BALANCE: ")
        print(self.balances)

        # SELL FROM BINANCE (SELLING ETH)
        size = order['bids']['size']
        price = order['bids']['price']
        binance.balances = ['ETH', -size]
        binance.balances = ['BTC', size * price]

        print("\nFINAL BALANCE: ")
        print(self.balances)
        final_balances = self.balances

        x = {key: final_balances[key] - start_balances.get(key, 0) for key in final_balances}
        print(f"TRADE COMPLETED {x}")

    def trade(self, order):
        print(order)

        # Works with only 1 bids exchange en 1 asks exchange
        asks = order['asks']
        bids = order['bids']
        asks_exchange = asks['exchange']
        asks_balance = asks_exchange.get_balances()
        bids_exchange = bids['exchange']
        bids_balance = bids_exchange.get_balances()

        # CHECK IF ENOUGH BALANCE
        # HARD CODED
        # Or check in previous function if size > balance ?

        # Buy from ASKS
        # This is the asks
        size = asks['size']
        asks_price = asks['price']
        asks_trading_pair = asks['trading_pair']
        try:
            print(f"Buying from {asks_exchange.name} {size} {asks_trading_pair[:3].upper()} @ {asks_price} {asks_trading_pair[-3:].upper()}")
            # asks_exchange.make_buy_order(asks_trading_pair, price, size)
        except Exception as err:
            print(err)
            print("ERROR: ASKS order error.")
            exit()

        # Sell from BIDS
        # size = round(order['bids']['size'] * (1 - settings.BUDA_FEE), 3)    For later: fix fees deduction
        bids_price = round(bids['price'], 6)
        bids_trading_pair = bids['trading_pair']
        try:
            print(f"Selling from {bids_exchange.name} {size} {bids_trading_pair[:3].upper()} @ {bids_price} {bids_trading_pair[-3:].upper()}")
            # bids_exchange.make_sell_order(bids_trading_pair, price, size)
        except Exception as err:
            print(err)
            print("ERROR: BIDS order error.")
            exit()

        print("TRADE COMPLETED")
        profit = (bids_price - asks_price) * size
        print(f"PROFIT of {'{0:.8f}'.format(profit)} {bids_trading_pair[-3:].upper()} - fees")
        exit()