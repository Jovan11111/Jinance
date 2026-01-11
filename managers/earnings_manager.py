from datetime import datetime, timedelta

import utils.constants as constants
from providers.earnings_provider import EarningsProvider


class EarningsManager:
    """Fetch upcoming earnings."""

    def __init__(
        self,
        days_ahead=30,
        tickers=constants.TICKERS_SP_100,
        provider: EarningsProvider = None,
    ):
        print("EarningsManager initialized")
        self._days_ahead = days_ahead
        self._tickers = tickers
        self._provider = provider

    @property
    def days_ahead(self):
        return self._days_ahead

    @property
    def tickers(self):
        return self._tickers

    @property
    def provider(self):
        return self._provider

    def get_latest_upcoming_earnings(self, number_of_companies):
        cutoff = datetime.today().date() + timedelta(days=self.days_ahead)
        earnings = self._provider.fetch_earnings(self.tickers, cutoff=cutoff)

        earnings.sort(key=lambda e: e.earnings_date)
        return earnings[:number_of_companies]
