import logging
from datetime import datetime, timedelta, timezone

from api.ai_service import AiService
from models.news_article import NewsArticle
from utils import constants

logger = logging.getLogger(__name__)


class NewsFilter:
    """Class responsible for filtering all provided news articles."""

    def __init__(self):
        logger.debug("NewsFilter initialized.")
        self.__seen_urls = set()
        self.__ai_service: AiService = AiService.get_instance()

    def filter_news(
        self, raw_news: list[NewsArticle], top_k: int, days_behind: int
    ) -> list[NewsArticle]:
        """Main method that filters all news articles on various criteria.

        Args:
            raw_news (list[NewsArticle]): all provided news articles
            top_k (int): number of articles to return
            days_behind (int): latest publication date cutoff in days

        Returns:
            list[NewsArticle]: List of filtered news articles
        """
        logger.debug("Starting news filtering process.")
        no_old_news = self.__filter_by_pub_date(raw_news, days_behind)
        no_seen_urls = self.__filter_by_seen_urls(no_old_news)
        with_keywords = self.__filter_by_keywords(no_seen_urls)
        with_ticker_in_title = self.__filter_by_ticker_in_title(with_keywords)
        ai_filtered_dicts = self.__ai_service.filter_news(with_ticker_in_title, top_k)
        return ai_filtered_dicts

    def __filter_by_pub_date(
        self, raw_news: list[NewsArticle], days_behind: int
    ) -> list[NewsArticle]:
        """Filter out news articles older than cutoff date."""
        logger.debug("Filtering news by publication date.")
        cutoff = self.__time_cutoff(days_behind)
        return [article for article in raw_news if article.pub_time >= cutoff]

    def __filter_by_seen_urls(self, raw_news: list[NewsArticle]) -> list[NewsArticle]:
        """Filter out news articles with same URLs"""
        logger.debug("Filtering news by seen URLs.")
        filtered_news = []
        for article in raw_news:
            if article.url not in self.__seen_urls:
                filtered_news.append(article)
                self.__seen_urls.add(article.url)
        return filtered_news

    def __filter_by_keywords(self, raw_news: list[NewsArticle]) -> list[NewsArticle]:
        """Filter out news articles that do not contain hard event keywords."""
        logger.debug("Filtering news by hard event keywords.")
        filtered_news = []
        for article in raw_news:
            title_l = article.title.lower()
            if any(keyword in title_l for keyword in constants.HARD_EVENT_KEYWORDS):
                filtered_news.append(article)
        return filtered_news

    def __filter_by_ticker_in_title(
        self, raw_news: list[NewsArticle]
    ) -> list[NewsArticle]:
        """Filter out news articles that do not mention ticker or company name in title."""
        logger.debug("Filtering news by ticker/company name in title.")
        filtered_news = []
        for article in raw_news:
            ticker_l = article.ticker.lower()
            company_name_l = constants.TICKER_TO_COMPANY[article.ticker]
            title_l = article.title.lower()
            if ticker_l in title_l or company_name_l in title_l:
                filtered_news.append(article)
        return filtered_news

    def __time_cutoff(self, days_behind) -> datetime:
        """Return datetime object representing cutoff date."""
        return datetime.now(timezone.utc) - timedelta(days=days_behind)
