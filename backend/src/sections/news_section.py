import logging

from managers.news_manager import NewsManager
from models.section_data import SectionData
from report_building.news_builder import NewsBuilder
from sections.report_section import ReportSection
from utils.localization import Localization

logger = logging.getLogger(__name__)


class NewsSection(ReportSection):
    """Class responsible for generating the news section of the report."""

    def __init__(self, section_data: SectionData):
        logger.debug("NewsSection initialized.")
        self.__manager = NewsManager(
            section_data.provider, section_data.days_behind, section_data.tickers
        )
        self.__builder = NewsBuilder(Localization(section_data.language))
        self.__number_of_articles = section_data.number_of_companies

    def generate(self) -> str:
        """Generate part of the report about latest news based on received data.

        Returns:
            str: .md formatted string containing the report part.
        """
        logger.debug("Generating News section of the report.")
        news_data = self.__manager.get_latest_news(self.__number_of_articles)
        return self.__builder.build_markdown(news_data)
