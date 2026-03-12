import logging
from typing import Dict

from filters.insider_info_filter import InsiderInfoFilter
from models.aggregated_insider_info import AggregatedInsiderInfo
from providers.yahoo.yahoo_insider_provider import YahooInsiderProvider
from utils import constants
from utils.enums.trade_type import TradeType

logger = logging.getLogger(__name__)


class InsiderManager:
    """Manages fetching and filtering insider trading data."""

    def __init__(
        self, provider: str = "yahoo", days_behind=30, tickers=constants.TICKERS_SP_100
    ):
        logger.debug("InsiderManager initialized.")
        self._tickers = tickers
        self._filter = InsiderInfoFilter(days_behind=days_behind)
        if provider == "yahoo":
            self._provider = YahooInsiderProvider()
        else:
            logger.warning(
                "Chose a non existent provider, initializing a default one..."
            )
            self._provider = YahooInsiderProvider()

    @property
    def tickers(self) -> list[str]:
        """Getter for tickers list."""
        return self._tickers

    @property
    def provider(self) -> YahooInsiderProvider:
        """Getter for insider provider."""
        return self._provider

    @property
    def filter(self) -> InsiderInfoFilter:
        """Getter for insider info filter."""
        return self._filter

    def get_insider_trades(
        self, number_of_companies: int
    ) -> Dict[str, list[AggregatedInsiderInfo]]:
        """Return list of biggest buyers and sellers for a specified number of companies.

        Args:
            number_of_companies (int): Number of buyers and sellers to return.

        Returns:
            Dict[str, list[FilteredInsiderInfo]]: Keys are buyers and sellers, values are lists of filtered insider trades.
        """
        if number_of_companies < 1:
            logger.warning(
                "Insufficient number of companies for insider trading, setting the value to default..."
            )
            number_of_companies = 3
        logger.debug(
            f"Fetching insider trading data for {number_of_companies} companies."
        )
        insider_trades = self.provider.fetch_insider_trades(self.tickers)
        filtered_insider_trades = self.filter.filter_insider_info(insider_trades)

        ticker_aggregation: Dict[str, Dict[str, int]] = {}
        for trade in filtered_insider_trades:
            if trade.ticker not in ticker_aggregation:
                ticker_aggregation[trade.ticker] = {"bought": 0, "sold": 0}

            if trade.type == TradeType.BUY:
                ticker_aggregation[trade.ticker]["bought"] += trade.value
            elif trade.type == TradeType.SELL:
                ticker_aggregation[trade.ticker]["sold"] += trade.value
        filtered_info_list = [
            AggregatedInsiderInfo(
                ticker=ticker, bought=values["bought"], sold=values["sold"]
            )
            for ticker, values in ticker_aggregation.items()
        ]

        return {
            "buyers": sorted(filtered_info_list, key=lambda x: x.bought, reverse=True)[
                :number_of_companies
            ],
            "sellers": sorted(filtered_info_list, key=lambda x: x.sold, reverse=True)[
                :number_of_companies
            ],
        }
