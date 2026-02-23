import logging
from datetime import datetime, timedelta

import utils.constants as constants
from models.earnings_information import EarningsInformation
from providers.earnings_provider import EarningsProvider
from providers.yahoo.yahoo_earnings_provider import YahooEarningsProvider

logger = logging.getLogger(__name__)


class EarningsManager:
    """Manages fetching earnings information."""

    def __init__(
        self,
        provider: str = "yahoo",
        days_ahead: int=30,
        tickers=constants.TICKERS_SP_100,
    ):
        logger.debug("EarnigsManager initialized.")
        self._days_ahead = days_ahead if days_ahead > 0 else 30
        self._tickers: list[str] = tickers
        if provider == "yahoo":
            self._provider: EarningsProvider = YahooEarningsProvider()
        else:
            logger.warning("Chose a non existant provider, initializing a default one...")
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
        logger.debug(
            f"Fetching latest upcoming earnings for {number_of_companies} companies."
        )
        cutoff = datetime.today().date() + timedelta(days=self.days_ahead)
        earnings = self.provider.fetch_earnings(self.tickers, cutoff=cutoff)

        earnings.sort(key=lambda e: e.date)
        return earnings[:number_of_companies]
