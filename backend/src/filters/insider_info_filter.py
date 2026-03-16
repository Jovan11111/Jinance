import logging
from datetime import datetime, timedelta

from models.insider_information import InsiderInformation
from utils.enums.trade_type import TradeType

logger = logging.getLogger(__name__)


class InsiderInfoFilter:
    """Class responsible for filtering all provided insider information."""

    def __init__(self, days_behind: int):
        logger.debug("InsiderInfoFilter initialized.")
        self.__cutoff = datetime.now() - timedelta(days=days_behind)

    def filter_insider_info(
        self, raw_insider_info: list[InsiderInformation]
    ) -> list[InsiderInformation]:
        """Filter insider trade info by leaving out old trades and gifts.

        Args:
            raw_insider_info (list[InsiderInformation]): Unfiltered insider info data.

        Returns:
            list[InsiderInformation]: Filtered insider info data.
        """
        recent_insider_info = self.__filter_by_recency(raw_insider_info)
        non_gift_insider_info = self.__filter_by_only_non_gifts(recent_insider_info)
        return non_gift_insider_info

    def __filter_by_recency(
        self, raw_insider_info: list[InsiderInformation]
    ) -> list[InsiderInformation]:
        """Remove insider information older than cutoff date."""
        logger.debug("Filtering insider info by recency.")
        return [trade for trade in raw_insider_info if trade.date >= self.__cutoff]

    def __filter_by_only_non_gifts(
        self, raw_insider_info: list[InsiderInformation]
    ) -> list[InsiderInformation]:
        """Remove all insider information about gifts (value = 0)."""
        logger.debug("Filtering out gift insider trades.")
        return [trade for trade in raw_insider_info if trade.type != TradeType.GIFT]
