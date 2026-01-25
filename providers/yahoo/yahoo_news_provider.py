import logging
from datetime import datetime

import yfinance as yf

from models.news_article import NewsArticle
from providers.news_provider import NewsProvider

logger = logging.getLogger(__name__)


class YahooNewsProvider(NewsProvider):
    """Class that provdes data about news articles by using yahoo finance API."""

    def fetch_news(self, tickers: list[str], days_behind: int) -> list[NewsArticle]:
        """Get all news articles posted on yahoo finance in the last **days_behind** days.

        Args:
            tickers (list[str]): Tickers for which to check news articles
            days_behind (int): How old can an article be to be included

        Returns:
            list[NewsArticle]: List of articles that have been posted in the last **days_behind** days.
        """
        logger.debug(
            f"Fetching all news in the last {days_behind} days using Yahoo Finance API."
        )
        result: list[NewsArticle] = []
        limit = self._news_limit(days_behind)

        for ticker in tickers:
            stock = yf.Ticker(ticker)
            news = stock.get_news(limit, "all")

            for article in news:
                content = article.get("content", {})
                if not content:
                    continue
                title = content.get("title", "")
                summary = content.get("summary", "")
                pub_date_str = content.get("pubDate", "1970-01-01T00:00:00Z")
                pub_date = datetime.fromisoformat(pub_date_str.replace("Z", "+00:00"))
                url = content.get("canonicalUrl", {}).get("url", "")
                result.append(NewsArticle(title, summary, pub_date, url, ticker))

        return result

    def _news_limit(self, days_behind: int) -> int:
        """Yahoo finance API for fetching news doesn't takes an argument limit which says how many articles it should return.
        This method returns estimated limit based on days_behind parameter."""
        if days_behind == 1:
            return 150
        if days_behind == 2:
            return 300
        return 1000
