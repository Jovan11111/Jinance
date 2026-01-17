from abc import ABC, abstractmethod
from datetime import datetime

from models.earnings_information import EarningsInformation


class EarningsProvider(ABC):
    """Interface used by all classes that provide Earnings data."""

    @abstractmethod
    def fetch_earnings(
        self, tickers: list[str], cutoff: datetime
    ) -> list[EarningsInformation]:
        """Return relevant future earnings data.

        Args:
            tickers (list[str]): List of tickers for which to check if there is an upcoming earnings report
            cutoff (datetime): Cutoff time for how away a report can be

        Returns:
            list[EarningsInformation]: List of relevant Earnings information.
        """
        pass
