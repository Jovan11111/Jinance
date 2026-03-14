import logging
from typing import Dict

from models.analyst_recommendation import AnalystRecommendation
from providers.yahoo.yahoo_analyst_provider import YahooAnalystProvider
from utils import constants
from utils.enums.provider_type import ProviderType

logger = logging.getLogger(__name__)


class AnalystManager:
    """Class that manages fetching and filtering analyst recommendations."""

    def __init__(
        self,
        provider: ProviderType = ProviderType.YAHOO,
        tickers: list[str] = constants.TICKERS_SP_100,
    ):
        logger.debug("AnalystManager initialized.")
        self._tickers = tickers
        if provider == ProviderType.YAHOO:
            self._provider = YahooAnalystProvider()
        else:
            logger.warning(
                "Chose a non existent provider, initializing a default one..."
            )
            self._provider = YahooAnalystProvider()

    @property
    def tickers(self) -> list[str]:
        """Getter for tickers list."""
        return self._tickers

    @property
    def provider(self) -> YahooAnalystProvider:
        """Getter for analyst provider."""
        return self._provider

    def get_analyst_recommendations(
        self, number_of_companies: int
    ) -> Dict[str, list[AnalystRecommendation]]:
        """Return list with number_of_companies top recommendations for buying and selling.

        Returns:
            Dict[str, list[AnalystRecommendation]]: Keys are buy and sell, values are lists of analyst recommendations.
        """
        if number_of_companies < 1:
            logger.warning(
                "Insufficient number of companies for analyst recommendations, setting the value to default..."
            )
            number_of_companies = 3

        logger.debug(
            f"Fetching analyst recommendations for {number_of_companies} companies."
        )

        recommendations = self.provider.fetch_analyst_recommendations(self.tickers)
        sorted_recommendations = sorted(
            recommendations, key=lambda x: x.index, reverse=True
        )

        return {
            "buy": sorted_recommendations[:number_of_companies],
            "sell": sorted_recommendations[-number_of_companies:],
        }
