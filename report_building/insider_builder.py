import logging
from typing import Dict

from models.aggregated_insider_info import AggregatedInsiderInfo
from report_building.report_builder import ReportBuilder
from utils.localization import Localization

logger = logging.getLogger(__name__)


class InsiderBuilder(ReportBuilder):
    """Class responsible for building the part of the report that contains relevant insider information in a .md format."""

    def __init__(self, localization: Localization):
        logger.debug("InsiderBuilder initialized.")
        super().__init__(localization)

    def build_markdown(
        self, insider_data: Dict[str, list[AggregatedInsiderInfo]]
    ) -> str:
        """Return .md formatted report part that includes all given insider information.

        Args:
            insider_data (Dict[str, list[AggregatedInsiderInfo]]): Information about relevant insider transactions that needs to be represented.

        Returns:
            str: String that contains all information in a formatted way.
        """
        logger.debug("Building insider markdown report part.")
        md: list[str] = []

        md.append(f"## {self._localization.translate("insider_title")}\n")
        md.append(f"{self._localization.translate("insider_intro")}\n")

        sellers = insider_data["sellers"]
        md.append(f"### {self._localization.translate('insider_sellers')}\n")
        md.append(
            f"| # | {self._localization.translate("insider_ticker")} | {self._localization.translate("insider_amount_sold")} |"
        )
        md.append("|---|--------|-------------|")
        for i, seller in enumerate(sellers, start=1):
            ticker = seller.ticker
            amount = seller.sold
            amount_str = f"${amount:,.0f}"
            md.append(f"| {i} | {ticker} | {amount_str} |")
        md.append("\n")

        buyers = insider_data["buyers"]
        md.append(f"### {self._localization.translate('insider_buyers')}\n")
        md.append(
            f"| # | {self._localization.translate("insider_ticker")} | {self._localization.translate("insider_amount_bought")} |"
        )
        md.append("|---|--------|---------------|")
        for i, buyer in enumerate(buyers, start=1):
            ticker = buyer.ticker
            amount = buyer.bought
            amount_str = f"${amount:,.0f}"
            md.append(f"| {i} | {ticker} | {amount_str} |")
        md.append("\n")

        md.append('<div class="page-break"></div>')

        return "\n".join(md)
