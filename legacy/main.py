from bot import Bot
from time import sleep
from buda import Buda
from binance_ import Binance


buda = Buda()

binance = Binance()
# print(binance.get_order_book("BTCUSDT"))
# exit()
# print(binance.get_balances())
# exit()

bot = Bot([buda, binance])
# tickers= ['ETH', 'BTC']
# bot.check_if_trade_available(tickers)
T = [['ETH', 'BTC'], ['LTC', 'BTC']]
for t in T:
    bot.check_if_trade_available(t)


