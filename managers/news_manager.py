from filters.news_filter import NewsFilter
from models.news_article import NewsArticle
from providers.news_provider import NewsProvider
from utils import constants


class NewsManager:
    """Fetch latest relevant news for given tickers."""

    def __init__(
        self,
        provider: NewsProvider,
        filter: NewsFilter,
        days_behind=1,
        tickers=constants.TICKERS_SP_100,
    ):
        print("NewsManager initialized")
        self.days_behind = days_behind
        self.tickers = tickers
        self.provider = provider
        self.filter = filter

    def get_latest_news(self) -> list[NewsArticle]:
        all_news = self.provider.fetch_news(self.tickers, self.days_behind)
        filtered_news = self.filter.filter_news(all_news, 10, self.days_behind)
        return filtered_news
