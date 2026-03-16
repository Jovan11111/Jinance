from abc import ABC, abstractmethod

from models.news_article import NewsArticle


class NewsProvider(ABC):
    """Interface for all classes that provide data about relevant news articles."""

    @abstractmethod
    def fetch_news(self, tickers: list[str], days_behind: int) -> list[NewsArticle]:
        """Get all news articles in a given time period.

        Args:
            tickers (list[str]): List of tickers for which to check news
            days_behind (int): How many days can the article be old.

        Returns:
            list[NewsArticle]: All news articles in a given time period.
        """
