import logging
from typing import Dict

from models.price_performance_information import PricePerformanceInformation
from providers.yahoo.yahoo_price_performance_provider import (
    YahooPricePerformanceProvider,
)
from utils import constants

logger = logging.getLogger(__name__)


class PricePerformanceManager:
    """Class that manages price performance for companies."""

    def __init__(self, provider: str, days_ahead=180, tickers=constants.TICKERS_SP_100):
        logger.debug("PricePerformanceManager initialized.")
        self._days_ahead = days_ahead
        self._tickers: list[str] = tickers
        if provider == "yahoo":
            self._provider = YahooPricePerformanceProvider()

    @property
    def days_ahead(self) -> int:
        """Getter for days_ahead."""
        return self._days_ahead

    @property
    def tickers(self) -> list[str]:
        """Getter for tickers."""
        return self._tickers

    @property
    def provider(self):
        """Getter for provider."""
        return self._provider

    def get_best_worst_price_performance(
        self, number_of_companies: int
    ) -> Dict[str, list[PricePerformanceInformation]]:
        """Returns best and worst performing companies in the given period.

        Args:
            number_of_companies (int): Number of winners and losers to return.

        Returns:
            Dict[str, list[PricePerformanceInformation]]: Keys: winners, losers, values are lists performances tied to tickers.
        """
        logger.debug(
            f"Fetching best and worst price performance for {number_of_companies} companies."
        )
        performances = self.provider.fetch_price_performance(
            self.tickers, self.days_ahead
        )
        performances.sort(key=lambda p: p.percent_change, reverse=True)

        return {
            "winners": performances[:number_of_companies],
            "losers": performances[-number_of_companies:],
        }
