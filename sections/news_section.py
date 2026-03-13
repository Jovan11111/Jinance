from managers.news_manager import NewsManager
from report_building.news_builder import NewsBuilder
from sections.report_section import ReportSection
from utils.enums.language import Language
from utils.localization import Localization


class NewsSection(ReportSection):
    """Class responsible for generating the news section of the report."""

    def __init__(
        self,
        provider: str,
        days_behind: int,
        tickers: list[str],
        language: Language,
        number_of_articles: int,
    ):
        self.__manager = NewsManager(provider, days_behind, tickers)
        self.__builder = NewsBuilder(Localization(language))
        self.__number_of_articles = number_of_articles

    def generate(self):
        news_data = self.__manager.get_latest_news(self.__number_of_articles)
        return self.__builder.build_markdown(news_data)
