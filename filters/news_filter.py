from datetime import datetime, timedelta, timezone

from api.ai_service import AiService
from models.news_article import NewsArticle
from utils import constants


class NewsFilter:

    def __init__(self):
        self._seen_urls = set()
        self.ai_service: AiService = AiService.get_instance()

    @property
    def seen_urls(self) -> set:
        return self._seen_urls

    def filter_news(
        self, raw_news: list[NewsArticle], top_k: int, days_behind: int
    ) -> list[NewsArticle]:
        no_old_news = self.filter_by_pub_date(raw_news, days_behind)
        no_seen_urls = self.filter_by_seen_urls(no_old_news)
        with_keywords = self.filter_by_keywords(no_seen_urls)
        with_ticker_in_title = self.filter_by_ticker_in_title(with_keywords)
        ai_filtered_dicts = self.ai_service.filter_news(with_ticker_in_title, top_k)
        return ai_filtered_dicts

    def filter_by_pub_date(
        self, raw_news: list[NewsArticle], days_behind: int
    ) -> list[NewsArticle]:
        cutoff = self._time_cutoff(days_behind)
        return [article for article in raw_news if article.pubDate >= cutoff]

    def filter_by_seen_urls(self, raw_news: list[NewsArticle]) -> list[NewsArticle]:
        filtered_news = []
        for article in raw_news:
            if article.url not in self._seen_urls:
                filtered_news.append(article)
                self._seen_urls.add(article.url)
        return filtered_news

    def filter_by_keywords(self, raw_news: list[NewsArticle]) -> list[NewsArticle]:
        filtered_news = []
        for article in raw_news:
            title_l = article.title.lower()
            if any(keyword in title_l for keyword in constants.HARD_EVENT_KEYWORDS):
                filtered_news.append(article)
        return filtered_news

    def filter_by_ticker_in_title(
        self, raw_news: list[NewsArticle]
    ) -> list[NewsArticle]:
        filtered_news = []
        for article in raw_news:
            ticker_l = article.ticker.lower()
            company_name_l = constants.TICKER_TO_COMPANY[article.ticker]
            title_l = article.title.lower()
            if ticker_l in title_l or company_name_l in title_l:
                filtered_news.append(article)
        return filtered_news

    def _time_cutoff(self, days_behind) -> datetime:
        return datetime.now(timezone.utc) - timedelta(days=days_behind)
