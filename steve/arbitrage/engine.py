from decimal import Decimal
from logging import getLogger
from operator import attrgetter

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


def run():
    exchanges = {el().__name__: el() for el in EXCHANGES}

    # available_balances = apply(exchanges, attrgetter("available_balances"))
    all_prices = apply(exchanges, attrgetter("prices"))

    for market in map(tuple, settings.MARKETS):
        prices = select(all_prices, market)

        bid_xcg_name, ask_xcg_name = find_best_trade(prices)

        # bid_exchange = exchanges[bid_xcg_name]
        # ask_exchange = exchanges[ask_xcg_name]

        bid_price, bid_amount = prices[bid_xcg_name][BID]
        ask_price, ask_amount = prices[ask_xcg_name][ASK]

        delta = (Decimal(bid_price) - Decimal(ask_price)) / Decimal(ask_price)

        logger.info(f"DELTA IN MARKET {market}: {round(100 * delta, 4)}%")
        logger.info(f"MIN DELTA: {100 * settings.MIN_DELTA}%")
        amount = min(bid_amount, ask_amount, settings.MAX_SIZE[market[0]])

        if delta > settings.MIN_DELTA:
            logger.info(f"PLACING ORDERS FOR {amount} {market[0]}")
            logger.info(f"Bought from {bid_xcg_name} {amount} @ {bid_price}")
            logger.info(f"Sold from {ask_xcg_name} {amount} @ {ask_price}")

            # bid_amount != ask_amount ; this will happen when fees are introduced
            # bid_exchange.place_limit_order(
            #     base=market[0],
            #     quote=market[1],
            #     side=BID,
            #     amount=amount,
            #     price=bid_price,
            # )
            # ask_exchange.place_limit_order(
            #     base=market[0],
            #     quote=market[1],
            #     side=ASK,
            #     amount=amount,
            #     price=ask_price,
            # )

    for exchange in exchanges.values():
        exchange.clear_cache()
