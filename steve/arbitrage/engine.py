import math
import threading as th
from decimal import Decimal
from logging import getLogger
from operator import attrgetter
from time import sleep

from django.conf import settings

from .exchanges import ASK, BID, EXCHANGES

logger = getLogger(__name__)

import requests
import json

class telegram_chatbot():

    def __init__(self, config=None):
        self.token = self.read_token_from_config_file(config)
        self.base = "https://api.telegram.org/bot{}/".format(self.token)

    def send_message(self, msg, chat_id):
        url = self.base + "sendMessage?chat_id={}&text={}".format(chat_id, msg)
        if msg is not None:
            requests.get(url)

    def read_token_from_config_file(self, config=None):
        return '1768966683:AAGtXy1_oUKnhohLhxeb-x97x9dTLUPz3YE'

bot = telegram_chatbot()
# telegram_id = '754457406' # Alex
telegram_id = '-276230411'

def apply(exchanges, func):
    return {xcg_name: func(exchange) for (xcg_name, exchange) in exchanges.items()}


def select(properties, inner_key):
    return {xcg_name: value[inner_key] for (xcg_name, value) in properties.items()}


def find_best_trade(market_prices):
    bids = {xcg_name: prices[BID] for (xcg_name, prices) in market_prices.items()}
    asks = {xcg_name: prices[ASK] for (xcg_name, prices) in market_prices.items()}

    bid_xcg_name = max(bids, key=lambda xcg_name: Decimal(bids[xcg_name][0]))
    ask_xcg_name = min(asks, key=lambda xcg_name: Decimal(asks[xcg_name][0]))

    return bid_xcg_name, ask_xcg_name


def get_total_balances(available_balances):
    total_balances = {}
    for xcg in available_balances.values():
        for ticker in xcg:
            if ticker not in total_balances:
                total_balances[ticker] = Decimal(xcg[ticker])
            else:
                total_balances[ticker] += Decimal(xcg[ticker])
    return total_balances


def filter_amount_by_stepsize(amount, market_symbol):
    step_size = Decimal(settings.STEP_SIZE[market_symbol].find("1") - 1)
    step_size_amount = math.floor(amount * 10 ** step_size) / (10 ** step_size)
    return max(step_size_amount, settings.MIN_SIZE[market_symbol])


def _execute(n=settings.LOOP_N):
    x = 0
    # for i in range(n):
    # bot.send_message("Bot started running.", telegram_id)
    while True:
        # sleep(1 )
        try:
            run()
        except Exception as err:
            x += 1
            bot.send_message(err, telegram_id)
            sleep(30)
            if x > 20:
                bot.send_message(f"Bot exited after {x} errors", telegram_id)
                exit()


def run():
    exchanges = {el().__name__: el() for el in EXCHANGES}

    available_balances = apply(exchanges, attrgetter("available_balances"))
    total_balances = get_total_balances(available_balances)
    all_prices = apply(exchanges, attrgetter("prices"))

    for market in map(tuple, settings.MARKETS):
        base, quote = market
        prices = select(all_prices, market)
        market_symbol = f"{base}{quote}"

        bid_xcg_name, ask_xcg_name = find_best_trade(prices)

        bid_exchange = exchanges[bid_xcg_name]
        ask_exchange = exchanges[ask_xcg_name]

        bid_balance = available_balances[bid_xcg_name][base]
        ask_balance = available_balances[ask_xcg_name][quote]

        bid_price, bid_amount = prices[bid_xcg_name][BID]
        ask_price, ask_amount = prices[ask_xcg_name][ASK]

        delta = (Decimal(bid_price) - Decimal(ask_price)) / Decimal(ask_price)

        ask_balance_transformed = Decimal(ask_balance) / Decimal(ask_price)

        if delta >= 0.05:
            mult = 5
        elif delta >= 0.04:
            mult = 3
        elif delta >= 0.03:
            mult = 2
        else:
            mult = 1

        amount = round(min(
            Decimal(bid_amount),
            Decimal(ask_amount),
            settings.MAX_SIZE[market_symbol] * mult,
            Decimal(bid_balance),
            ask_balance_transformed,
        ),5)
        logger.info(
            f"DELTA IN MARKET {market_symbol}: {round(100 * delta, 4)}% | {amount}"
        )
        # bot.send_message(f"DELTA IN MARKET {market_symbol}: {round(100 * delta, 4)}% | {amount}", '754457406')
        # logger.info(f"MIN DELTA: {100 * settings.MIN_DELTA}%")

        if delta >= settings.MIN_DELTA and amount >= settings.MIN_SIZE[market_symbol]:
            logger.info(f"PLACING ORDERS FOR {amount} {base}")
            logger.info(f"Starting balances {total_balances}")

            # Check if enough balance for trade
            # ask_balance_transformed = Decimal(ask_balance) / Decimal(ask_price)
            if (
                amount <= Decimal(bid_balance)
                and Decimal(amount) < ask_balance_transformed
            ):
                ask_amount = filter_amount_by_stepsize(Decimal(amount), market_symbol)
                if (amount * settings.FEES) >= Decimal(settings.STEP_SIZE[market_symbol]):
                    bid_amount = filter_amount_by_stepsize(
                        amount * (1 - settings.FEES), market_symbol
                    )
                else:
                    bid_amount = ask_amount
                type_msg = "Binance filled at LIMIT"
                # bid_amount != ask_amount ; this will happen when fees are introduced
                # bid_order_id = bid_exchange.place_limit_order(
                bid_order_id, type_ = bid_exchange.place_market_order(
                    base=base,
                    quote=quote,
                    side=BID,
                    amount=bid_amount,
                    price=bid_price,
                )
                if type_ == 0:
                    type_msg = "Binance filled at MARKET"
                # ask_order_id = ask_exchange.place_limit_order(
                ask_order_id, type_ = ask_exchange.place_market_order(
                    base=base,
                    quote=quote,
                    side=ASK,
                    amount=ask_amount,
                    price=ask_price,
                )
                if type_ == 0:
                    type_msg = "Binance filled at MARKET"
                # bid_status = bid_exchange.order_filled(bid_order_id, base, quote)
                # ask_status = ask_exchange.order_filled(ask_order_id, base, quote)
                bid_status = True
                ask_status = True
                if bid_status and ask_status:
                    logger.info(
                        (
                            f"{bid_order_id} | Sold from {bid_xcg_name} {bid_amount}"
                            f" @ {bid_price}"
                        )
                    )
                    logger.info(
                        (
                            f"{ask_order_id} | Bought from {ask_xcg_name} {ask_amount}"
                            f" @ {ask_price}"
                        )
                    )
                    msg = (
                            f"PLACING ORDERS FOR {amount} {base} WITH DELTA {round(100 * delta, 4)}%\n"
                            f"{bid_order_id} | Sold from {bid_xcg_name} {bid_amount}"
                            f" @ {bid_price}\n"
                            f"{ask_order_id} | Bought from {ask_xcg_name} {ask_amount}"
                            f" @ {ask_price}"
                            f"| {type_msg}"
                    )
                    bot.send_message(msg, telegram_id)
                    exchanges = {el().__name__: el() for el in EXCHANGES}
                    available_balances = apply(
                        exchanges, attrgetter("available_balances")
                    )
                    total_balances = get_total_balances(available_balances)
                    logger.info(f"Final balances {total_balances}")
                    # exit()
                    if delta < 0.04:
                        sleep(5)
                    # break
                else:
                    logger.warning("ERROR in transaction")
                    logger.info(ask_order_id, bid_order_id)
                    logger.info(ask_status, bid_status)
                    bot.send_message("Bot exited with error", telegram_id)
                    exit()
            else:
                logger.warning(
                    f"Not enough balance for {market} trade. Trade amount was {amount}"
                )
                logger.warning(available_balances)
                bot.send_message(f"BALANCE ERROR for {market} trade. Trade amount was {amount}", telegram_id)
                # exit()
    for exchange in exchanges.values():
        exchange.clear_cache()


def execute(async_):
    if async_:
        thread = th.Thread(target=_execute)
        thread.start()
        return thread

    else:
        return _execute()
