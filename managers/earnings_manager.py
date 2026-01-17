from datetime import datetime, timedelta

import utils.constants as constants
from models.earnings_information import EarningsInformation
from providers.yahoo_earnings_provider import YahooEarningsProvider


class EarningsManager:
    """Fetch upcoming earnings."""

    def __init__(
        self,
        provider: str,
        days_ahead=30,
        tickers=constants.TICKERS_SP_100,
    ):
        print("EarningsManager initialized")
        self._days_ahead = days_ahead
        self._tickers = tickers
        if provider == "yahoo":
            self._provider = YahooEarningsProvider()

    @property
    def days_ahead(self):
        return self._days_ahead

    @property
    def tickers(self):
        return self._tickers

    @property
    def provider(self):
        return self._provider

    def get_latest_upcoming_earnings(
        self, number_of_companies
    ) -> list[EarningsInformation]:
        cutoff = datetime.today().date() + timedelta(days=self.days_ahead)
        earnings = self._provider.fetch_earnings(self.tickers, cutoff=cutoff)

        earnings.sort(key=lambda e: e.date)
        return earnings[:number_of_companies]
