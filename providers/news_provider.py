from abc import ABC, abstractmethod

from models.news_article import NewsArticle


class NewsProvider(ABC):

    @abstractmethod
    def fetch_news(self, tickers: list[str], days_behind: int) -> list[NewsArticle]:
        pass
