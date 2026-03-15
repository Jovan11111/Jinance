from datetime import datetime

from utils.enums.trade_type import TradeType


class InsiderInformation:
    """Class that represents information about a single insider trade.

    Fields:
        ticker (str): Ticker of the company the insider information is about.
        value (float): Value of the insider trade.
        type (TradeType): Shows if stock was bought or sold or given.
        date (datetime): Date when the trade occurred.
    """

    def __init__(
        self,
        ticker: str,
        value: float,
        type: TradeType,
        date: datetime,
    ):
        self.__ticker: str = ticker
        self.__value: float = value if value >= 0 else 0
        self.__type: TradeType = type
        self.__date: datetime = date

    @property
    def ticker(self) -> str:
        """Getter for the ticker of the insider trading information."""
        return self.__ticker

    @property
    def value(self) -> float:
        """Getter for the value of the insider trading information."""
        return self.__value

    @property
    def type(self) -> TradeType:
        """Getter for the type of the insider trading information."""
        return self.__type

    @property
    def date(self) -> datetime:
        """Getter for the date of the insider trading information."""
        return self.__date

    def to_dict(self) -> dict:
        """Convert InsiderInformation object to a dictionary."""
        return {
            "ticker": self.ticker,
            "value": self.__value,
            "type": self.__type,
            "date": self.date.isoformat(),
        }
