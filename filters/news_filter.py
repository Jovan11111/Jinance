from datetime import datetime, timedelta, timezone

from api.ai_service import AiService
from models.news_article import NewsArticle
from utils import constants


class NewsFilter:
    """Class responsible for filtering all provided news articles."""

    def __init__(self):
        self._seen_urls = set()
        self.ai_service: AiService = AiService.get_instance()

    @property
    def seen_urls(self) -> set:
        """Getter for seen URLs set."""
        return self._seen_urls

    def filter_news(
        self, raw_news: list[NewsArticle], top_k: int, days_behind: int
    ) -> list[NewsArticle]:
        """Main mathod that filters all news articles on various criteria.

        Args:
            raw_news (list[NewsArticle]): all provided news articles
            top_k (int): number of articles to return
            days_behind (int): latest publication date cutoff in days

        Returns:
            list[NewsArticle]: List of filtered news articles
        """
        no_old_news = self._filter_by_pub_date(raw_news, days_behind)
        no_seen_urls = self._filter_by_seen_urls(no_old_news)
        with_keywords = self._filter_by_keywords(no_seen_urls)
        with_ticker_in_title = self._filter_by_ticker_in_title(with_keywords)
        ai_filtered_dicts = self.ai_service.filter_news(with_ticker_in_title, top_k)
        return ai_filtered_dicts

    def _filter_by_pub_date(
        self, raw_news: list[NewsArticle], days_behind: int
    ) -> list[NewsArticle]:
        """Filter out news articles older than cutoff date."""
        cutoff = self._time_cutoff(days_behind)
        return [article for article in raw_news if article.pub_time >= cutoff]

    def _filter_by_seen_urls(self, raw_news: list[NewsArticle]) -> list[NewsArticle]:
        """Filter out news articles with same URLs"""
        filtered_news = []
        for article in raw_news:
            if article.url not in self.seen_urls:
                filtered_news.append(article)
                self.seen_urls.add(article.url)
        return filtered_news

    def _filter_by_keywords(self, raw_news: list[NewsArticle]) -> list[NewsArticle]:
        """Filter out news articles that do not contain hard event keywords."""
        filtered_news = []
        for article in raw_news:
            title_l = article.title.lower()
            if any(keyword in title_l for keyword in constants.HARD_EVENT_KEYWORDS):
                filtered_news.append(article)
        return filtered_news

    def _filter_by_ticker_in_title(
        self, raw_news: list[NewsArticle]
    ) -> list[NewsArticle]:
        """Filter out news articles that do not mention ticker or company name in title."""
        filtered_news = []
        for article in raw_news:
            ticker_l = article.ticker.lower()
            company_name_l = constants.TICKER_TO_COMPANY[article.ticker]
            title_l = article.title.lower()
            if ticker_l in title_l or company_name_l in title_l:
                filtered_news.append(article)
        return filtered_news

    def _time_cutoff(self, days_behind) -> datetime:
        """Return datetime object representing cutoff date."""
        return datetime.now(timezone.utc) - timedelta(days=days_behind)
