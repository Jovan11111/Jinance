from datetime import datetime, timedelta, timezone

import yfinance as yf

from api.ai_service import AiService
from utils import constants


class NewsManager:
    """Fetch latest relevant news for given tickers."""

    def __init__(self, days_behind=1, tickers=constants.TICKERS_SP_100):
        print("NewsManager initialized")
        self.days_behind = days_behind
        self.tickers = tickers
        self.ai_service = AiService.get_instance()

    def _news_limit(self) -> int:
        if self.days_behind == 1:
            return 150
        if self.days_behind == 2:
            return 300
        return 1000

    def _time_cutoff(self) -> datetime:
        return datetime.now(timezone.utc) - timedelta(days=self.days_behind)

    def get_latest_news(self) -> dict:
        result = {}
        seen_urls = set()

        limit = self._news_limit()
        cutoff = self._time_cutoff()

        for ticker in self.tickers:
            stock = yf.Ticker(ticker)
            company_name = constants.TICKER_TO_COMPANY.get(ticker, "").lower()

            news = stock.get_news(limit, "all")
            if not news:
                continue

            ticker_news = []

            for article in news:
                content = article.get("content", {})

                title = content.get("title", "")
                summary = content.get("summary", "")
                pub_date = content.get("pubDate")
                link = content.get("canonicalUrl", {}).get("url")

                if not title or not pub_date or not link:
                    continue

                if link in seen_urls:
                    continue

                title_l = title.lower()

                if ticker.lower() not in title_l and company_name not in title_l:
                    continue

                pub_time = datetime.fromisoformat(pub_date.replace("Z", "+00:00"))

                if pub_time < cutoff:
                    continue

                if not any(
                    keyword in title_l for keyword in constants.HARD_EVENT_KEYWORDS
                ):
                    continue

                ticker_news.append(
                    {
                        "pubTime": pub_time,
                        "title": title,
                        "summary": summary,
                        "link": link,
                    }
                )

                seen_urls.add(link)

            if ticker_news:
                result[ticker] = ticker_news

        print(len(seen_urls))
        print("\n===== FINAL NEWS OUTPUT =====")
        from pprint import pprint

        small_res = self.ai_service.filter_news(result, top_k=10)
        pprint(small_res)

        return result
