from datetime import datetime

from models.eps_information import EpsInformation
from models.previous_earnings_information import PreviousEarningsInformation


class EarningsInformation:
    """Dataclass that represents earnings information that is to be displayed.

    Fields:
        ticker (str): Ticker of the company the earnings information is about.
        name (str): Name of the company the earning information is about.
        value_last_15_days (list[float]): Value of the company in the last 15 days.
        market_cap (int): Market cap of the company.
        eps (EpsInformation): Estimated earnings per share of the company.
        date (datetime): Date of the earnings report.
        revenue (int): Revenue of the company.
        previous_earnings (list[PreviousEarningsInformation]): List of previous 4 earnings, their expected and actual EPS.
    """

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
        self.__ticker: str = ticker
        self.__name: str = name
        self.__value_last_15_days: list[float] = value_last_15_days
        self.__market_cap: int = market_cap if market_cap >= 0 else 0
        self.__eps: EpsInformation = eps
        self.__date: datetime = date
        self.__revenue: int = revenue if revenue >= 0 else 0
        self.__previous_earnings: list[PreviousEarningsInformation] = previous_earnings

    @property
    def ticker(self) -> str:
        """Getter for ticker symbol of the company."""
        return self.__ticker

    @property
    def name(self) -> str:
        """Getter for company name."""
        return self.__name

    @property
    def value_last_15_days(self) -> list[float]:
        """Getter for stock prices in the last 15 days."""
        return self.__value_last_15_days

    @property
    def market_cap(self) -> int:
        """Getter for market capitalization of the company."""
        return self.__market_cap

    @property
    def eps(self) -> EpsInformation:
        """Getter for Earnings Per Share information."""
        return self.__eps

    @property
    def date(self) -> datetime:
        """Getter for earnings announcement date."""
        return self.__date

    @property
    def revenue(self) -> int:
        """Getter for company revenue."""
        return self.__revenue

    @property
    def previous_earnings(self) -> list[PreviousEarningsInformation]:
        """Getter for previous earnings EPS information."""
        return self.__previous_earnings

    def to_dict(self) -> dict:
        """Convert the EarningsInformation object to a dictionary."""
        return {
            "ticker": self.__ticker,
            "name": self.__name,
            "value_last_15_days": self.__value_last_15_days,
            "market_cap": self.__market_cap,
            "eps": self.__eps.to_dict(),
            "date": self.__date.isoformat() if self.date else "",
            "revenue": self.__revenue,
            "previous_earnings": [
                prev_earn.to_dict() for prev_earn in self.__previous_earnings
            ],
        }
