from datetime import date
import os

from report_building.graph_builder import GraphBuilder
from utils.singleton_meta import SingletonMeta
import markdown as md_pkg
from weasyprint import HTML

class ReportBuilder(metaclass=SingletonMeta):
    def __init__(self):
        print("ReportBuilder initialized")
        self.graph_builder: GraphBuilder = GraphBuilder.get_instance()

    def build_markdown(self, data: dict) -> str:
        today = date.today().strftime("%d.%m.%Y")

        md = []
        md.append(f"# Izveštaj za {today}")
        md.append("## Earnings izveštaj\n")
        md.append("Ovo je automatski generisan izveštaj o nadolazećim javnim objavama prihoda, u kom su prikazani osnovni podaci o narednih 5 firmi koje ce javno objaviti prihode. Podaci su dohvaceni sa yahoo finance besplatne pristupne tacke.\n")
        for idx, (ticker, info) in enumerate(data.items()):
            name = info.get("name", "")
            earnings_date = info.get("date", "")
            eps = info.get("eps", [])
            market_cap = info.get("market_cap", 0)
            revenue = info.get("revenue", 0)
            prices = info.get("value_last_15_days", [])
            prev_eps = info.get("previous_earnings", [])
            expected_vals = [round(el.get("expected_eps"), 2) for el in prev_eps]
            actual_vals = [round(el.get("actual_eps"), 2) for el in prev_eps]
            price_changes = [round(el.get("price_diff"), 2) for el in prev_eps]
            eps_avg = eps[0] if eps else 0
            eps_low = eps[1] if eps else 0
            eps_high = eps[2] if eps else 0

            graph_path = self.graph_builder.build_price_graph(prices, ticker)

            md.append(f"### {name} - {ticker}")
            md.append(f"- **Datum earnings-a:** {earnings_date.strftime('%d.%m.%Y')}")
            md.append(f"- **Prosečna EPS:** {eps_avg}")
            md.append(f"- **Pesimistična EPS:** {eps_low}")
            md.append(f"- **Optimistična EPS:** {eps_high}")

            md.append("\n**Prethodni EPS**\n")
            md.append("| | najskoriji | -> | -> | najstariji |")
            md.append("|---|---|---|---|---|")
            md.append(f"| **Ocekivani** | {expected_vals[0]} | {expected_vals[1]} | {expected_vals[2]} | {expected_vals[3]} |")
            md.append(f"| **Stvarni** | {actual_vals[0]} | {actual_vals[1]} | {actual_vals[2]} | {actual_vals[3]} |")
            md.append(f"| **Promena cene (%)** | {price_changes[0]} | {price_changes[1]} | {price_changes[2]} | {price_changes[3]} |")
            md.append("\n")
            md.append(f"- **Vrednost firme:** ${market_cap:,}")
            md.append(f"- **Prihod firme:** ${revenue:,}")

            if graph_path:
                md.append("\n**Cena akcije poslednjih 15 dana:**\n")
                md.append(f"![Price chart]({graph_path})")

            # insert a page break so each company starts on its own page (except after last)
            if idx != len(data) - 1:
                md.append('<div class="page-break"></div>')

        return "\n".join(md)

    def create_pdf_report(self, data: dict) -> str:
        md_content = self.build_markdown(data)

        today_str = date.today().strftime("%Y%m%d")

        html_body = md_pkg.markdown(md_content, extensions=["extra", "nl2br"]) 

        html = (
            "<!doctype html><html><head><meta charset='utf-8'>"
            "<style>"
            "body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial; padding: 1rem; }"
            "img { max-width: 100% !important; height: auto !important; display: block; margin: 0 auto 1rem; }"
            "table { border-collapse: collapse; margin: 1rem 0; width: 100%; }"
            "th, td { border: 1px solid #333; padding: 6px 10px; text-align: center; }"
            "th { background-color: #f0f0f0; font-weight: bold; }"
            "tr:nth-child(even) { background-color: #fafafa; }"
            "/* Page break helper: used between company sections */"
            ".page-break { page-break-after: always; break-after: page; }"
            "@page { size: A4; margin: 1cm; }"
            "</style></head><body>"
            f"{html_body}</body></html>"
        )
        pdf_path = f"report_{today_str}.pdf"

        HTML(string=html, base_url=os.getcwd()).write_pdf(pdf_path)

        return pdf_path
