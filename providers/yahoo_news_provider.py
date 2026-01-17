from datetime import datetime

import yfinance as yf

from models.news_article import NewsArticle
from providers.news_provider import NewsProvider


class YahooNewsProvider(NewsProvider):
    def fetch_news(self, tickers: list[str], days_behind: int) -> list[NewsArticle]:
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
                pub_date_str = content.get("pubDate")
                pub_date = datetime.fromisoformat(pub_date_str.replace("Z", "+00:00"))
                url = content.get("canonicalUrl", {}).get("url")
                result.append(NewsArticle(title, summary, pub_date, url, ticker))

        return result

    def _news_limit(self, days_behind: int) -> int:
        if days_behind == 1:
            return 150
        if days_behind == 2:
            return 300
        return 1000
