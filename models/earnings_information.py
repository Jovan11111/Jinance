from datetime import datetime

from models.eps_information import EpsInformation
from models.previous_earnings_information import PreviousEarningsInformation


class EarningsInformation:
    """Dataclass that represents earnings information that is to be displayed."""

    def __init__(
        self,
        ticker: str,
        name: str,
        value_last_15_days: list[float],
        market_cap: int,
        eps: EpsInformation,
        date: datetime,
        revenue: int,
        previous_earnings: list[PreviousEarningsInformation],
    ):
        self._ticker: str = ticker
        self._name: str = name
        self._value_last_15_days: list[float] = value_last_15_days
        self._market_cap: int = market_cap
        self._eps: EpsInformation = eps
        self._date: datetime = date
        self._revenue: int = revenue
        self._previous_earnings: list[PreviousEarningsInformation] = previous_earnings

    @property
    def ticker(self) -> str:
        """Getter for ticker symbol of the company."""
        return self._ticker

    @property
    def name(self) -> str:
        """Getter for company name."""
        return self._name

    @property
    def value_last_15_days(self) -> list[float]:
        """Getter for stock prices in the last 15 days."""
        return self._value_last_15_days

    @property
    def market_cap(self) -> int:
        """Getter for market capitalization of the company."""
        return self._market_cap

    @property
    def eps(self) -> EpsInformation:
        """Getter for Earnings Per Share information."""
        return self._eps

    @property
    def date(self) -> datetime:
        """Getter for earnings announcement date."""
        return self._date

    @property
    def revenue(self) -> int:
        """Getter for company revenue."""
        return self._revenue

    @property
    def previous_earnings(self) -> list[PreviousEarningsInformation]:
        """Getter for previous earnings EPS information."""
        return self._previous_earnings

    def to_dict(self) -> dict:
        """Convert the EarningsInformation object to a dictionary."""
        return {
            "ticker": self._ticker,
            "name": self._name,
            "value_last_15_days": self._value_last_15_days,
            "market_cap": self._market_cap,
            "eps": self._eps.to_dict(),
            "date": self._date.isoformat(),
            "revenue": self._revenue,
            "previous_earnings": [
                prev_earn.to_dict() for prev_earn in self._previous_earnings
            ],
        }
