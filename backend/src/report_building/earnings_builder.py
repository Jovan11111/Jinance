import logging

from models.earnings_information import EarningsInformation
from report_building.graph_builder import GraphBuilder
from report_building.report_builder import ReportBuilder
from utils.localization import Localization

logger = logging.getLogger(__name__)


class EarningsBuilder(ReportBuilder):
    """Class responsible for creating a part of the report that includes Earnings information in .md format."""

    def __init__(self, localization: Localization):
        logger.debug("EarningsBuilder initialized.")
        self.__graph_builder = GraphBuilder(localization)
        super().__init__(localization)

    def build_markdown(self, earnings_data: list[EarningsInformation]) -> str:
        """Returns .md formatted report part that includes all given upcoming earnings information.

        Args:
            earnings_data (list[EarningsInformation]): Information about upcoming earnings that needs to be represented.

        Returns:
            str: String that contains all information in a formatted way.
        """
        logger.debug("Building earnings markdown report part.")
        md = []
        md.append(f"## {self._localization.translate("earnings_title")}\n")
        md.append(f"{self._localization.translate("earnings_intro")}\n")
        for earning in earnings_data:
            graph_path = self.__graph_builder.build_price_graph(
                earning.value_last_15_days, earning.ticker
            )

            md.append(f"### {earning.name} - {earning.ticker}")
            md.append(
                f"- **{self._localization.translate("earnings_date")}** {earning.date.strftime('%d.%m.%Y')}"
            )
            if earning.eps is not None:
                md.append(
                    f"- **{self._localization.translate("earnings_eps_avg")}** {earning.eps.avg}"
                )
                md.append(
                    f"- **{self._localization.translate("earnings_eps_low")}** {earning.eps.low}"
                )
                md.append(
                    f"- **{self._localization.translate("earnings_eps_high")}** {earning.eps.high}"
                )
            else:
                md.append(
                    f"- **{self._localization.translate("earnings_eps_avg")}** N/A"
                )
                md.append(
                    f"- **{self._localization.translate("earnings_eps_low")}** N/A"
                )
                md.append(
                    f"- **{self._localization.translate("earnings_eps_high")}** N/A"
                )

            md.append(f"\n**{self._localization.translate("earnings_prev_eps")}**\n")
            md.append(
                f"| | {self._localization.translate("earnings_latest")} | -> | -> | {self._localization.translate("earnings_oldest")} |"
            )
            md.append("|---|---|---|---|---|")
            helper_row = (
                f"| **{self._localization.translate("earnings_prev_eps_expected")}** |"
            )
            for prev in earning.previous_earnings:
                helper_row += f" {prev.expected_eps} |"
            md.append(helper_row)

            helper_row = (
                f"| **{self._localization.translate("earnings_prev_eps_actual")}** |"
            )
            for prev in earning.previous_earnings:
                helper_row += f" {prev.actual_eps} |"
            md.append(helper_row)

            helper_row = (
                f"| **{self._localization.translate("earnings_prev_eps_diff")}** |"
            )
            for prev in earning.previous_earnings:
                helper_row += f" {prev.price_diff} |"
            md.append(helper_row)

            md.append("\n")
            market_cap_str = (
                f"${earning.market_cap:,}" if earning.market_cap is not None else "N/A"
            )
            revenue_str = (
                f"${earning.revenue:,}" if earning.revenue is not None else "N/A"
            )
            md.append(
                f"- **{self._localization.translate("earnings_market_cap")}** {market_cap_str}"
            )
            md.append(
                f"- **{self._localization.translate("earnings_revenue")}** {revenue_str}"
            )

            if graph_path:
                md.append(
                    f"\n**{self._localization.translate("earnings_price_chart")}**\n"
                )
                md.append(f"![Price chart]({graph_path})")

            md.append('<div class="page-break"></div>')

            md.append("\n")
        return "\n".join(md)
