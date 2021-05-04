import math
import threading as th
from decimal import Decimal
from logging import getLogger
from operator import attrgetter
from time import sleep

from django.conf import settings

from .exchanges import ASK, BID, EXCHANGES

logger = getLogger(__name__)


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



def _excecute(n=settings.LOOP_N):
    for i in range(n):
        sleep(1)
        run()


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

        logger.info(f"DELTA IN MARKET {market_symbol}: {round(100 * delta, 4)}%")
        logger.info(f"MIN DELTA: {100 * settings.MIN_DELTA}%")
        amount = min(
            Decimal(bid_amount),
            Decimal(ask_amount),
            settings.MAX_SIZE[market_symbol],
        )
        if delta >= settings.MIN_DELTA and amount >= settings.MIN_SIZE[market_symbol]:
            logger.info(f"PLACING ORDERS FOR {amount} {base}")
            logger.info(f"Starting balances {total_balances}")

            # Check if enough balance for trade
            ask_balance_transformed = Decimal(ask_balance) / Decimal(ask_price)
            if (
                amount <= Decimal(bid_balance)
                and Decimal(amount) <= ask_balance_transformed
            ):
                ask_amount = filter_amount_by_stepsize(Decimal(amount), market_symbol)
                if (amount * settings.FEES) >= Decimal(settings.STEP_SIZE[market_symbol]):
                    bid_amount = filter_amount_by_stepsize(
                        amount * (1 - settings.FEES), market_symbol
                    )
                else:
                    bid_amount = ask_amount
                # bid_amount != ask_amount ; this will happen when fees are introduced
                # bid_order_id = bid_exchange.place_limit_order(
                bid_order_id = bid_exchange.place_market_order(
                    base=base,
                    quote=quote,
                    side=BID,
                    amount=bid_amount,
                    price=bid_price,
                )
                # ask_order_id = ask_exchange.place_limit_order(
                ask_order_id = ask_exchange.place_market_order(
                    base=base,
                    quote=quote,
                    side=ASK,
                    amount=ask_amount,
                    price=ask_price,
                )
                bid_status = bid_exchange.order_filled(bid_order_id, base, quote)
                ask_status = ask_exchange.order_filled(ask_order_id, base, quote)
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
                    exchanges = {el().__name__: el() for el in EXCHANGES}
                    available_balances = apply(
                        exchanges, attrgetter("available_balances")
                    )
                    total_balances = get_total_balances(available_balances)
                    logger.info(f"Final balances {total_balances}")
                    break
                else:
                    logger.warning("ERROR in transaction")
                    logger.info(ask_order_id, bid_order_id)
                    logger.info(ask_status, bid_status)
            else:
                logger.warning(
                    f"Not enough balance for {market} trade. Trade amount was {amount}"
                )
    for exchange in exchanges.values():
        exchange.clear_cache()


def execute(async_):
    if async_:
        thread = th.Thread(target=_execute)
        thread.start()
        return thread

    else:
        return _execute()
