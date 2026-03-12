import logging

import yfinance as yf

from models.analyst_recommendation import AnalystRecommendation
from providers.analyst_provider import AnalystProvider

logger = logging.getLogger(__name__)


class YahooAnalystProvider(AnalystProvider):
    """Class that retrieves analyst recommendations for ticker with yahoo finance API."""

    def fetch_analyst_recommendations(
        self, tickers: list[str]
    ) -> list[AnalystRecommendation]:
        """Return analyst recommendations for given tickers by using yahoo finance API.

        Args:
            tickers (list[str]): List of tickers for which to retrieve analyst recommendations.

        Returns:
            list[AnalystRecommendation]: List of analyst recommendations for the given tickers.
        """

        analyst_recommendations: list[AnalystRecommendation] = []

        for ticker in tickers:
            try:
                stock = yf.Ticker(ticker)
                mean = stock.info.get("recommendationMean", -1.0)
                if mean < 1 or mean > 5:
                    logger.warning(
                        f"Invalid mean value for ticker {ticker}: {mean}. Skipping."
                    )
                    continue

                analyst_recommendations.append(
                    AnalystRecommendation(
                        ticker=ticker, index=self.__mean_to_index(mean)
                    )
                )
            except Exception as e:
                logger.warning(f"Error fetching analyst recommendations: {e}")
                continue

        return analyst_recommendations

    def __mean_to_index(self, mean: float) -> float:
        """Convert mean retrieved from api to index used in jinance.

        Mean in yfinance is between 1 and 5, where 1 is a strong buy and 5 is a strong sell.
        Index in jinance is between 100 and -100 where 100 is a strong buy, and -100 is a strong sell.

        Args:
            mean (float): Mean that is retrieved from yahoo finance API.

        Returns:
            float: Converted index used in jinance.
        """
        return -50.0 * (mean - 3.0)
