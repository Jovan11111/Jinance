from abc import ABC, abstractmethod

from models.insider_information import InsiderInformation


class InsiderProvider(ABC):
    """Interface used by all classes that provide Insider data."""

    @abstractmethod
    def fetch_insider_trades(
        self, tickers: list[str], days_behind: int
    ) -> list[InsiderInformation]:
        """Return relevant insider trading data.

        Args:
            tickers (list[str]): List of tickers for which to check if there are any recent insider trades
            days_behind (int): How old can an insider trade be to be included
        Returns:
            list[InsiderInformation]: List of relevant insider trading information.
        """
