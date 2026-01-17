from datetime import datetime, timedelta

import utils.constants as constants
from models.earnings_information import EarningsInformation
from providers.earnings_provider import EarningsProvider
from providers.yahoo_earnings_provider import YahooEarningsProvider


class EarningsManager:
    """Manages fetching earnings information."""

    def __init__(
        self,
        provider: str,
        days_ahead=30,
        tickers=constants.TICKERS_SP_100,
    ):
        self._days_ahead = days_ahead
        self._tickers: list[str] = tickers
        if provider == "yahoo":
            self._provider: EarningsProvider = YahooEarningsProvider()

    @property
    def days_ahead(self) -> int:
        """Getter for days_ahead."""
        return self._days_ahead

    @property
    def tickers(self) -> list[str]:
        """Getter for tickers."""
        return self._tickers

    @property
    def provider(self) -> EarningsProvider:
        """Getter for provider."""
        return self._provider

    def get_latest_upcoming_earnings(
        self, number_of_companies: int
    ) -> list[EarningsInformation]:
        """Returns specified number of latest upcoming earnings reports

        Args:
            number_of_companies (_type_): Number of companies to return

        Returns:
            list[EarningsInformation]: List of EarningsInformation objects that contain earnings data.
        """
        cutoff = datetime.today().date() + timedelta(days=self.days_ahead)
        earnings = self._provider.fetch_earnings(self.tickers, cutoff=cutoff)

        earnings.sort(key=lambda e: e.date)
        return earnings[:number_of_companies]
