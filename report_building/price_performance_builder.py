from typing import Dict

from models.price_performance_information import PricePerformanceInformation
from report_building.graph_builder import GraphBuilder
from report_building.report_builder import ReportBuilder
from utils import constants


class PricePerformanceBuilder(ReportBuilder):
    """Class that create a part of the report that includes price performance information in .md format."""

    def __init__(self):
        self._graph_builder = GraphBuilder()

    @property
    def graph_builder(self) -> GraphBuilder:
        """Getter for GraphBuilder object used to create graphs that are included."""
        return self._graph_builder

    def build_markdown(
        self, price_perf_data: Dict[str, list[PricePerformanceInformation]]
    ) -> str:
        """Returns .md formatted string that includes price performance information about winners and losers

        Args:
            price_perf_data (list[PricePerformanceInformation]): Information about price performance that needs to be represented.

        Returns:
            str: String that contains all information in a formatted way.
        """
        md = []
        md.append("## Izvestaj od najboljim i najgorim performansama cena akcija\n")
        md.append(
            "Ovo je automatski generisan izveštaj o najboljim i najgorim performansama cena akcija na berzi u poslednjih 6 meseci.\n"
        )
        md.append("### Najbolje performanse cena akcija\n")
        for price_perf in price_perf_data["winners"]:
            graph_path = self.graph_builder.build_price_graph(
                price_perf.prices, price_perf.ticker
            )

            md.append(
                f"**{constants.TICKER_TO_COMPANY[price_perf.ticker]} - {price_perf.ticker}**"
            )
            md.append(f"- Cena pre 6 meseci: {price_perf.prices[0]}")
            md.append(f"- Trenutna cena: {price_perf.prices[-1]}")
            md.append(
                f"- Promena cene u poslednjih 6 meseci (%): {price_perf.percent_change}\n"
            )
            md.append(f"![Grafik performansi cene]({graph_path})\n")

        for price_perf in price_perf_data["losers"]:
            graph_path = self.graph_builder.build_price_graph(
                price_perf.prices, price_perf.ticker
            )

            md.append(
                f"**{constants.TICKER_TO_COMPANY[price_perf.ticker]} - {price_perf.ticker}**"
            )
            md.append(f"- Cena pre 6 meseci: {price_perf.prices[0]}")
            md.append(f"- Trenutna cena: {price_perf.prices[-1]}")
            md.append(
                f"- Promena cene u poslednjih 6 meseci: {price_perf.percent_change} %\n"
            )
            md.append(f"![Grafik performansi cene]({graph_path})\n")

        return "\n".join(md)
