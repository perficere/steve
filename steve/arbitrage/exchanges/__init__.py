from .base import ASK, BID  # noqa: F401
from .binance import Interface as Binance
from .buda import Interface as Buda

EXCHANGES = [Binance, Buda]
