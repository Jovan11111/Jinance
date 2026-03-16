import logging
import os
from datetime import date

import markdown as md_pkg
from weasyprint import HTML

from models.section_data import SectionData
from sections.analyst_section import AnalystSection
from sections.earnings_section import EarningsSection
from sections.insider_section import InsiderSection
from sections.news_section import NewsSection
from sections.price_performance_section import PricePerformanceSection
from sections.report_section import ReportSection
from utils.enums.language import Language
from utils.enums.section_type import SectionType
from utils.localization import Localization

logger = logging.getLogger(__name__)


class ReportBuilderDirector:
    """Class responsible for putting together the whole report and converting it into PDF."""

    SECTION_CLASS_MAP = {
        SectionType.EARNINGS: EarningsSection,
        SectionType.NEWS: NewsSection,
        SectionType.PRICE_PERFORMANCE: PricePerformanceSection,
        SectionType.INSIDER_TRADES: InsiderSection,
        SectionType.ANALYST_RATINGS: AnalystSection,
    }

    def __init__(self, language: Language):
        logger.debug("ReportBuilderDirector initialized.")
        self.__localization = Localization(language)

    def __build_markdown(self, section_data: list[SectionData]) -> str:
        """Creates a whole report in .md format by calling all sections it contains."""
        logger.debug("Building markdown content for the report.")
        today = date.today().strftime("%d.%m.%Y")

        md = []

        md.append(f"# {self.__localization.translate("report_title")} {today}")

        for section in section_data:
            new_section: ReportSection = self.SECTION_CLASS_MAP[section.type](section)
            md.append(new_section.generate())

        return "\n".join(md)

    def create_pdf_report(self, section_data: list[SectionData]) -> str:
        """Creates a pdf report that is a final produce of the whole application.

        Args:
            section_data (list[SectionData]): Information about sections that are supposed to be in the report.

        Returns:
            str: path to a pdf report that is created and saved.
        """
        logger.debug("Creating PDF report.")
        md_content = self.__build_markdown(section_data)
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
