import os
from datetime import date

import markdown as md_pkg
from weasyprint import HTML

from models.earnings_information import EarningsInformation
from models.news_article import NewsArticle
from report_building.earnings_buidler import EarningsBuilder
from report_building.news_builder import NewsBuilder


class ReportBuilderDirector:
    def __init__(
        self,
    ):
        self._earnings_builder = EarningsBuilder()
        self._news_builder = NewsBuilder()

    @property
    def earnings_builder(self) -> EarningsBuilder:
        return self._earnings_builder

    def build_markdown(
        self, earnings_data: list[EarningsInformation], news_data: list[NewsArticle]
    ) -> str:
        today = date.today().strftime("%d.%m.%Y")

        md = []
        md.append(f"# Izveštaj za {today}")
        md.append(self.earnings_builder.build_markdown(earnings_data))
        md.append(self._news_builder.build_markdown(news_data))
        return "\n".join(md)

    def create_pdf_report(
        self, earnings_data: list[EarningsInformation], news_data: list[NewsArticle]
    ) -> str:
        md_content = self.build_markdown(earnings_data, news_data)

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
