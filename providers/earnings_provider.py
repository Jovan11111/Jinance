from abc import ABC, abstractmethod
from datetime import datetime

from models.earnings_information import EarningsInformation


class EarningsProvider(ABC):

    @abstractmethod
    def fetch_earnings(
        self, tickers: list[str], cutoff: datetime
    ) -> list[EarningsInformation]:
        pass
