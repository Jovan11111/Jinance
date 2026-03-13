import logging
import os
from datetime import date

import markdown as md_pkg
from weasyprint import HTML

from models.report_information import ReportInformation
from utils.enums.language import Language

logger = logging.getLogger(__name__)


class ReportBuilderDirector:
    """Class responsible for putting together the whole report and converting it into PDF."""

    def __init__(self, language: Language = Language.SERBIAN):
        logger.debug("ReportBuilderDirector initialized.")

    def _build_markdown(
        self,
    ) -> str:
        """Creates a whole report in .md format by calling all other builders it contains."""
        logger.debug("Building markdown content for the report.")
        today = date.today().strftime("%d.%m.%Y")

        md = []
        md.append(f"# {self.localization.translate("report_title")} {today}")

        return "\n".join(md)

    def create_pdf_report(self, report_info: ReportInformation) -> str:
        """Creates a pdf report that is a final produce of the whole application.

        Args:
            earnings_data (list[EarningsInformation]): Data about earnings that is supposed to be represented.
            news_data (list[NewsArticle]): Data about news that is supposed to be represented.

        Returns:
            str: path to a pdf report that is created and saved.
        """
        logger.debug("Creating PDF report.")
        md_content = ""

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
