import logging

from filters.news_filter import NewsFilter
from models.news_article import NewsArticle
from providers.yahoo.yahoo_news_provider import YahooNewsProvider
from utils import constants

logger = logging.getLogger(__name__)


class NewsManager:
    """Manages fetching and filtering news articles."""

    def __init__(
        self,
        provider: str,
        days_behind=1,
        tickers=constants.TICKERS_SP_100,
    ):
        logger.debug("NewsManager initialized.")
        self.days_behind = days_behind
        self.tickers = tickers
        if provider == "yahoo":
            self.provider = YahooNewsProvider()
        self.filter = NewsFilter()

    def get_latest_news(self) -> list[NewsArticle]:
        """Returns 10 most important news in the selected time period.

        Returns:
            list[NewsArticle]: List of news articles.
        """
        logger.debug(
            f"Fetching latest news articles in the last {self.days_behind} days."
        )
        all_news = self.provider.fetch_news(self.tickers, self.days_behind)
        filtered_news = self.filter.filter_news(all_news, 10, self.days_behind)
        return filtered_news
