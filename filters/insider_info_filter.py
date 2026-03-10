import logging
from datetime import datetime, timedelta

from models.insider_information import InsiderInformation
from utils.enums.trade_type import TradeType

logger = logging.getLogger(__name__)


class InsiderInfoFilter:
    """Class responsible for filtering all provided insider information."""

    def __init__(self, days_behind: int):
        logger.debug("InsiderInfoFilter initialized.")
        self._cutoff = datetime.now() - timedelta(days=days_behind)

    @property
    def cutoff(self) -> datetime:
        """Getter for cutoff date."""
        return self._cutoff

    def filter_insider_info(
        self, raw_insider_info: list[InsiderInformation]
    ) -> list[InsiderInformation]:
        recent_insider_info = self._filter_by_recency(raw_insider_info)
        non_gift_insider_info = self._filter_by_only_non_gifts(recent_insider_info)
        return non_gift_insider_info

    def _filter_by_recency(
        self, raw_insider_info: list[InsiderInformation]
    ) -> list[InsiderInformation]:
        """Remove insider information older than cutoff date."""
        return [trade for trade in raw_insider_info if trade.date >= self.cutoff]

    def _filter_by_only_non_gifts(
        self, raw_insider_info: list[InsiderInformation]
    ) -> list[InsiderInformation]:
        """Remove all insider information about gifts (value = 0)."""
        return [trade for trade in raw_insider_info if trade.type != TradeType.GIFT]
