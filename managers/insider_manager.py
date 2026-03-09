import logging
from typing import Dict

from models.insider_information import InsiderInformation
from providers.yahoo.yahoo_insider_provider import YahooInsiderProvider
from utils import constants

logger = logging.getLogger(__name__)


class InsiderManager:
    """Manages fetching and filtering insider trading data."""

    def __init__(
        self, provider: str = "yahoo", days_behind=7, tickers=constants.TICKERS_SP_100
    ):
        logger.debug("InsiderManager initialized.")
        self.days_behind = days_behind if days_behind > 0 else 7
        self.tickers = tickers
        if provider == "yahoo":
            self.provider = YahooInsiderProvider()
        else:
            logger.warning(
                "Chose a non existent provider, initializing a default one..."
            )
            self.provider = YahooInsiderProvider()

    def get_insider_trades(
        self, number_of_companies: int
    ) -> Dict[str, list[InsiderInformation]]:
        """Returns list of biggest buyers and sellers for a specified number of companies.

        Args:
            number_of_companies (int): Number of buyers and sellers to return.

        Returns:
            Dict[str, list[InsiderInformation]]: Keys are buyers and sellers, values are lists of insider trades tied to a ticker.
        """
        if number_of_companies < 1:
            logger.warning(
                "Insufficient number of companies for insider trading, setting the value to default..."
            )
            number_of_companies = 3
        logger.debug(
            f"Fetching insider trading data for {number_of_companies} companies."
        )
        insider_trades = self.provider.fetch_insider_trades(
            self.tickers, self.days_behind
        )

        # TODO add sorting of data
        # Sort first by buying then take the first x companies, then by selling and take the first x companies.

        return {
            "buyers": insider_trades[:number_of_companies],
            "sellers": insider_trades[-number_of_companies:],
        }
