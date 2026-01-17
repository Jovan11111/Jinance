from models.earnings_information import EarningsInformation
from report_building.graph_builder import GraphBuilder
from report_building.report_builder import ReportBuilder


class EarningsBuilder(ReportBuilder):
    def __init__(self):
        self._graph_builder = GraphBuilder()

    @property
    def graph_builder(self) -> GraphBuilder:
        return self._graph_builder

    def build_markdown(self, earnings_data: list[EarningsInformation]) -> str:
        md = []
        md.append("## Earnings izveštaj\n")
        md.append(
            "Ovo je automatski generisan izveštaj o nadolazećim javnim objavama prihoda, u kom su prikazani osnovni podaci o narednih 5 firmi koje ce javno objaviti prihode. Podaci su dohvaceni sa yahoo finance besplatne pristupne tacke.\n"
        )
        for earning in earnings_data:
            graph_path = self.graph_builder.build_price_graph(
                earning.value_last_15_days, earning.ticker
            )

            md.append(f"### {earning.name} - {earning.ticker}")
            md.append(f"- **Datum earnings-a:** {earning.date.strftime('%d.%m.%Y')}")
            md.append(f"- **Prosečna EPS:** {earning.eps.avg}")
            md.append(f"- **Pesimistična EPS:** {earning.eps.low}")
            md.append(f"- **Optimistična EPS:** {earning.eps.high}")

            md.append("\n**Prethodni EPS**\n")
            md.append("| | najskoriji | -> | -> | najstariji |")
            md.append("|---|---|---|---|---|")
            helper_row = "| **Ocekivani** |"
            for prev in earning.previous_earnings:
                helper_row += f" {prev.expected_eps} |"
            md.append(helper_row)

            helper_row = "| **Stvarni** |"
            for prev in earning.previous_earnings:
                helper_row += f" {prev.actual_eps} |"
            md.append(helper_row)

            helper_row = "| **Promena cene (%)** |"
            for prev in earning.previous_earnings:
                helper_row += f" {prev.price_diff} |"
            md.append(helper_row)

            md.append("\n")
            md.append(f"- **Vrednost firme:** ${earning.market_cap:,}")
            md.append(f"- **Prihod firme:** ${earning.revenue:,}")

            if graph_path:
                md.append("\n**Cena akcije poslednjih 15 dana:**\n")
                md.append(f"![Price chart]({graph_path})")

            md.append('<div class="page-break"></div>')

            md.append("\n")
        return "\n".join(md)
