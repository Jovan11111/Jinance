import logging

from models.news_article import NewsArticle
from report_building.report_builder import ReportBuilder
from utils.localization import Localization

logger = logging.getLogger(__name__)


class NewsBuilder(ReportBuilder):
    """Class responsible for building the part of the report that conatins relevant news information in a .md format."""

    def __init__(self, localization: Localization):
        logger.debug("NewsBuilder initialized.")
        self.localization = localization

    def build_markdown(self, news_data: list[NewsArticle]) -> str:
        """Returns .md formated report part that includes all given news information.

        Args:
            news_data (list[NewsArticle]): Information about relevant news articles that needs to be represented.

        Returns:
            str: String that contains all information in a formated way.
        """
        logger.debug("Building news markdown report part.")
        md: list[str] = []

        md.append(f"## {self.localization.translate("news_title")}\n")
        md.append(f"{self.localization.translate("news_intro")}\n")

        for article in news_data:
            md.append(f"### [{article.title}]({article.url}) - {article.ticker}\n")
            md.append(
                f"{self.localization.translate("news_date")}: {article.pub_time.strftime('%d.%m.%Y %H:%M')}\n"
            )
            md.append(f"{article.summary}\n")
            md.append("---\n")

        md.append('<div class="page-break"></div>')

        return "\n".join(md)
