import logging
from typing import Dict

from models.analyst_recommendation import AnalystRecommendation
from report_building.report_builder import ReportBuilder
from utils.localization import Localization

logger = logging.getLogger(__name__)


class AnalystBuilder(ReportBuilder):
    """Class responsible for building the part of the report that contains analyst recommendations."""

    def __init__(self, localization: Localization):
        logger.debug("AnalystBuilder initialized.")
        self.localization = localization

    def build_markdown(
        self, analyst_recommendations: Dict[str, list[AnalystRecommendation]]
    ) -> str:
        """Return .md formatted report part that includes a table of biggest but/sell recommendations.

        Args:
            analyst_recommendations (Dict[str, list[AnalystRecommendation]]): Recommendations that need to be in the table.

        Returns:
            str: String that contains all information in .md format.
        """

        logger.debug("Building analyst recommendations markdown report part.")
        md: list[str] = []
        md.append(f"## {self.localization.translate("analyst_title")}\n")
        md.append(f"{self.localization.translate("analyst_intro")}\n")

        buys = analyst_recommendations["buy"]
        sells = analyst_recommendations["sell"]
        md.append(f"### {self.localization.translate("analyst_sells")}\n")
        md.append(
            f"| # | {self.localization.translate("analyst_ticker")} | {self.localization.translate("analyst_index")}  |"
        )
        md.append("|---|--------|-----------------------|")
        for i, recommendation in enumerate(sells, start=1):
            ticker = recommendation.ticker
            index = recommendation.index
            index_str = f"{index:.2f}"
            md.append(f"| {i} | {ticker} | {index_str} |")
        md.append("\n")

        md.append(f"### {self.localization.translate("analyst_buys")}\n")
        md.append(
            f"| # | {self.localization.translate("analyst_ticker")} | {self.localization.translate("analyst_index")}  |"
        )
        md.append("|---|--------|-----------------------|")
        for i, recommendation in enumerate(buys, start=1):
            ticker = recommendation.ticker
            index = recommendation.index
            index_str = f"{index:.2f}"
            md.append(f"| {i} | {ticker} | {index_str} |")

        md.append("\n")

        md.append('<div class="page-break"></div>')

        return "\n".join(md)
