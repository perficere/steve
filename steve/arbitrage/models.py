from django.db import models

from core.base import BaseModel


class OrderSide(models.IntegerChoices):
    BID, ASK = range(2)


class OrderType(models.IntegerChoices):
    LIMIT, MARKET = range(2)


class Order(BaseModel):
    base = models.CharField(max_length=50, verbose_name="market base ticker")
    quote = models.CharField(max_length=50, verbose_name="market quote ticker")

    side = models.SmallIntegerField(choices=OrderSide.choices, verbose_name="side")
    type = models.SmallIntegerField(choices=OrderType.choices, verbose_name="type")


class Trade(BaseModel):
    pass
