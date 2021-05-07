from django.db import models

from core.base import BaseModel


class ExchangeName(models.TextChoices):
    BINANCE = "Binance"
    BUDA = "Buda"


class OrderType(models.TextChoices):
    LIMIT = "Limit"
    MARKET = "Market"


class OrderSide(models.TextChoices):
    BID = "Bid"
    ASK = "Ask"


class Ticker(models.TextChoices):
    BTC = ("BTC",)
    ETH = ("ETH",)
    LTC = ("LTC",)


class Order(BaseModel):
    remote_id = models.PositiveBigIntegerField(verbose_name="remote ID")
    exchange_name = models.CharField(
        choices=ExchangeName.choices, max_length=50, verbose_name="exchange name"
    )

    state = models.CharField(max_length=50, verbose_name="state")

    type = models.SmallIntegerField(choices=OrderType.choices, verbose_name="type")
    side = models.SmallIntegerField(choices=OrderSide.choices, verbose_name="side")
    price = models.DecimalField(max_digits=10, decimal_places=8, verbose_name="price")

    original_amount = models.DecimalField(
        max_digits=5, decimal_places=3, verbose_name="original amount"
    )
    traded_amount = models.DecimalField(
        max_digits=5, decimal_places=3, verbose_name="traded amount"
    )

    fee = models.DecimalField(max_digits=5, decimal_places=5, verbose_name="paid fee")

    @property
    def __str__(self):
        return f"{self.side} #{self.trade.pk}"


class Trade(BaseModel):
    id = models.BigAutoField(
        editable=False, primary_key=True, serialize=False, unique=True, verbose_name="ID"
    )

    base = models.CharField(
        choices=Ticker.choices, max_length=50, verbose_name="market base ticker"
    )
    quote = models.CharField(
        choices=Ticker.choices, max_length=50, verbose_name="market quote ticker"
    )

    bid_order = models.OneToOneField(
        to="arbitrage.Order", verbose_name="bid-side order", on_delete=models.PROTECT
    )
    ask_order = models.OneToOneField(
        to="arbitrage.Order", verbose_name="ask-side order", on_delete=models.PROTECT
    )

    @property
    def absolute_price_delta(self):
        return self.bid_order.price - self.ask_order.price

    @property
    def relative_price_delta(self):
        return self.absolute_price_delta / self.ask_order.price

    @property
    def total_fee(self):
        return self.bid_order.fee + self.ask_order.fee

    @property
    def profit(self):
        self.bid_order.traded_amount - self.ask_order.traded_amount - self.total_fee

    @property
    def market(self):
        return (self.base, self.quote)

    @property
    def market_symbol(self):
        return f"{self.base}-{self.quote}"

    def __str__(self):
        return str(self.pk)
