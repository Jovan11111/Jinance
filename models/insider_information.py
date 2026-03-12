from datetime import datetime

from utils.enums.trade_type import TradeType


class InsiderInformation:
    """Class that represents information about insider trading that is in the report."""

    def __init__(
        self,
        ticker: str,
        value: float,
        type: TradeType,
        date: datetime,
    ):
        self._ticker: str = ticker
        self._value: float = value if value >= 0 else 0
        self._type: TradeType = type
        self._date: datetime = date

    @property
    def ticker(self) -> str:
        """Getter for the ticker of the insider trading information."""
        return self._ticker

    @property
    def value(self) -> float:
        """Getter for the value of the insider trading information."""
        return self._value

    @property
    def type(self) -> TradeType:
        """Getter for the type of the insider trading information."""
        return self._type

    @property
    def date(self) -> datetime:
        """Getter for the date of the insider trading information."""
        return self._date

    def to_dict(self) -> dict:
        """Convert InsiderInformation object to a dictionary."""
        return {
            "ticker": self.ticker,
            "value": self._value,
            "type": self._type,
            "date": self.date.isoformat(),
        }
