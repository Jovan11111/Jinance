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
        provider: str = "yahoo",
        days_behind=1,
        tickers=constants.TICKERS_SP_100,
    ):
        logger.debug("NewsManager initialized.")
        self.days_behind = days_behind if days_behind > 0 else 1
        self.tickers = tickers
        if provider == "yahoo":
            self.provider = YahooNewsProvider()
        else:
            logger.warning(
                "Chose a non existent provider, initializing a default one..."
            )
            self.provider = YahooNewsProvider()
        self.filter = NewsFilter()

    def get_latest_news(self, number_of_articles: int) -> list[NewsArticle]:
        """Returns the specified number of most important news articles in the selected time period.

        Args:
            number_of_articles (int): The number of articles to return.

        Returns:
            list[NewsArticle]: List of news articles.
        """
        logger.debug(
            f"Fetching latest news articles in the last {self.days_behind} days."
        )
        all_news = self.provider.fetch_news(self.tickers, self.days_behind)
        filtered_news = self.filter.filter_news(
            all_news, number_of_articles, self.days_behind
        )
        return filtered_news
