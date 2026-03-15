from enum import Enum


class TradeType(Enum):
    """Enumeration that shows the type of insider trade.

    Type:
        BUY: Insider bought stock.
        SELL: Insider sold stock.
        GIFT: Insider was gifted stock.
    """

    BUY = "buy"
    SELL = "sell"
    GIFT = "gift"
