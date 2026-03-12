from abc import ABC, abstractmethod

from models.analyst_recommendation import AnalystRecommendation


class AnalystProvider(ABC):
    """Interface used by all classes that provide Analyst recommendation data."""

    @abstractmethod
    def fetch_analyst_recommendations(
        self, tickers: list[str]
    ) -> list[AnalystRecommendation]:
        """Return analyst recommendations for given tickers.

        Args:
            tickers (list[str]): List of tickers for which to retrieve analyst recommendations.

        Returns:
            list[AnalystRecommendation]: List of analyst recommendations for the given tickers.
        """
