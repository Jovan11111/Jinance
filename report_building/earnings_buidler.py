from models.earnings_information import EarningsInformation
from report_building.graph_builder import GraphBuilder
from report_building.report_builder import ReportBuilder


class EarningsBuilder(ReportBuilder):
    def __init__(self, earnings_data: list[EarningsInformation]):
        self._graph_builder = GraphBuilder()
        self._earnings_data = earnings_data

    @property
    def earnings_data(self) -> list[EarningsInformation]:
        return self._earnings_data

    def build_markdown(self) -> str:
        md = []
        md.append("## Earnings izveštaj\n")
        md.append(
            "Ovo je automatski generisan izveštaj o nadolazećim javnim objavama prihoda, u kom su prikazani osnovni podaci o narednih 5 firmi koje ce javno objaviti prihode. Podaci su dohvaceni sa yahoo finance besplatne pristupne tacke.\n"
        )
        for earning in self.earnings_data:
            md.append(f"### {earning.name} - {earning.ticker}")
            md.append(f"- **Datum earnings-a:** {earning.date.strftime('%d.%m.%Y')}")
            md.append(f"- **Prosečna EPS:** {earning.eps.avg}")
            md.append(f"- **Pesimistična EPS:** {earning.eps.low}")
            md.append(f"- **Optimistična EPS:** {earning.eps.high}")

            md.append("\n**Prethodni EPS**\n")
            md.append("| | najskoriji | -> | -> | najstariji |")
            md.append("|---|---|---|---|---|")
            """
            md.append(
                f"| **Ocekivani** | {expected_vals[0]} | {expected_vals[1]} | {expected_vals[2]} | {expected_vals[3]} |"
            )
            md.append(
                f"| **Stvarni** | {actual_vals[0]} | {actual_vals[1]} | {actual_vals[2]} | {actual_vals[3]} |"
            )
            md.append(
                f"| **Promena cene (%)** | {price_changes[0]} | {price_changes[1]} | {price_changes[2]} | {price_changes[3]} |"
            )
            md.append("\n")
            md.append(f"- **Vrednost firme:** ${market_cap:,}")
            md.append(f"- **Prihod firme:** ${revenue:,}")

            if graph_path:
                md.append("\n**Cena akcije poslednjih 15 dana:**\n")
                md.append(f"![Price chart]({graph_path})")

            # insert a page break so each company starts on its own page (except after last)
            if idx != len(data) - 1:
                md.append('<div class="page-break"></div>')
            """

            md.append("\n")
        return "\n".join(md)
