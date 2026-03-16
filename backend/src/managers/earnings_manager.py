import logging
from datetime import datetime, timedelta

import utils.constants as constants
from models.earnings_information import EarningsInformation
from providers.earnings_provider import EarningsProvider
from providers.yahoo.yahoo_earnings_provider import YahooEarningsProvider
from utils.enums.provider_type import ProviderType

logger = logging.getLogger(__name__)


class EarningsManager:
    """Manages fetching earnings information."""

    def __init__(
        self,
        provider: ProviderType = ProviderType.YAHOO,
        days_ahead: int = 30,
        tickers=constants.TICKERS_SP_100,
    ):
        logger.debug("EaringsManager initialized.")
        self.__days_ahead = days_ahead if days_ahead > 0 else 30
        self.__tickers: list[str] = tickers
        if provider == ProviderType.YAHOO:
            self.__provider: EarningsProvider = YahooEarningsProvider()
        else:
            logger.warning(
                "Chose a non existent provider, initializing a default one..."
            )
            self.__provider: EarningsProvider = YahooEarningsProvider()

    def get_latest_upcoming_earnings(
        self, number_of_companies: int
    ) -> list[EarningsInformation]:
        """Returns specified number of latest upcoming earnings reports.

        Args:
            number_of_companies (int): Number of earnings to return.

        Returns:
            list[EarningsInformation]: List of EarningsInformation objects that contain earnings data.
        """
        logger.debug(
            f"Fetching latest upcoming earnings for {number_of_companies} companies."
        )
        cutoff = datetime.today().date() + timedelta(days=self.__days_ahead)
        earnings = self.__provider.fetch_earnings(self.__tickers, cutoff=cutoff)
        earnings = [e for e in earnings if e is not None and e.date is not None]
        earnings.sort(key=lambda e: e.date)
        return earnings[:number_of_companies]
