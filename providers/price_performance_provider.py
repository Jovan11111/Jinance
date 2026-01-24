from abc import ABC, abstractmethod

from models.price_performance_information import PricePerformanceInformation


class PricePerformanceProvider(ABC):
    """Interface for all classes that provide data about price performance."""

    @abstractmethod
    def fetch_price_performance(
        self, tickers: list[str], days_behind: int
    ) -> list[PricePerformanceInformation]:
        """Get prices for all tickers in a given time period.

        Args:
            tickers (list[str]): List of tickers for which to get prices.
            days_behind (int): How many days behind to get prices for.

        Returns:
            list[PricePerformanceInformation]: List of price performances for all tickers.
        """
