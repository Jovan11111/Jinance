from datetime import datetime, timezone
from unittest.mock import MagicMock

import pytest

from providers.yahoo.yahoo_news_provider import YahooNewsProvider


@pytest.fixture
def mock_yf_ticker(mocker):
    return mocker.patch("providers.yahoo.yahoo_news_provider.yf.Ticker")


class TestYahooNewsProvider:
    def test__news_limit__returns_correct_limits(self):
        provider = YahooNewsProvider()

        assert provider._news_limit(1) == 150
        assert provider._news_limit(2) == 300
        assert provider._news_limit(5) == 1000
        assert provider._news_limit(10) == 1000

    def test__fetch_news_multiple_tickers__returns_all_news(self, mock_yf_ticker):
        mock_stock_1 = MagicMock()
        mock_stock_2 = MagicMock()
        mock_stock_3 = MagicMock()

        mock_stock_1.get_news.return_value = [
            {
                "content": {
                    "title": "News 1 for TCK1",
                    "summary": "this is summary",
                    "pubDate": "2025-09-04T12:00:00Z",
                    "canonicalUrl": {"url": "http://news1.com"},
                }
            }
        ]

        mock_stock_2.get_news.return_value = [
            {
                "content": {
                    "title": "News 1 for TCK2",
                    "summary": "this is summary",
                    "pubDate": "2025-09-03T12:00:00Z",
                    "canonicalUrl": {"url": "http://news2.com"},
                }
            },
            {
                "content": {
                    "title": "News 2 for TCK2",
                    "summary": "this is summary",
                    "pubDate": "2025-09-02T12:00:00Z",
                    "canonicalUrl": {"url": "http://news3.com"},
                }
            },
        ]

        mock_stock_3.get_news.return_value = [
            {
                "content": {
                    "title": "News 1 for TCK3",
                    "summary": "this is summary",
                    "pubDate": "2025-09-01T12:00:00Z",
                    "canonicalUrl": {"url": "http://news4.com"},
                }
            },
            {
                "content": {
                    "title": "News 2 for TCK3",
                    "summary": "this is summary",
                    "pubDate": "2025-08-31T12:00:00Z",
                    "canonicalUrl": {"url": "http://news5.com"},
                }
            },
            {
                "content": {
                    "title": "News 3 for TCK3",
                    "summary": "this is summary",
                    "pubDate": "2025-08-30T12:00:00Z",
                    "canonicalUrl": {"url": "http://news6.com"},
                }
            },
        ]

        def ticker_side_effect(ticker):
            mapping = {"TCK1": mock_stock_1, "TCK2": mock_stock_2, "TCK3": mock_stock_3}
            return mapping[ticker]

        mock_yf_ticker.side_effect = ticker_side_effect

        provider = YahooNewsProvider()
        result = provider.fetch_news(["TCK1", "TCK2", "TCK3"], days_behind=3)
        assert len(result) == 6
        assert result[0].ticker == "TCK1"
        assert result[0].title == "News 1 for TCK1"
        assert result[0].summary == "this is summary"
        assert result[0].pub_time == datetime(2025, 9, 4, 12, 0, tzinfo=timezone.utc)
        assert result[0].url == "http://news1.com"
        assert result[1].ticker == "TCK2"
        assert result[1].title == "News 1 for TCK2"
        assert result[1].summary == "this is summary"
        assert result[1].pub_time == datetime(2025, 9, 3, 12, 0, tzinfo=timezone.utc)
        assert result[1].url == "http://news2.com"
        assert result[2].ticker == "TCK2"
        assert result[2].title == "News 2 for TCK2"
        assert result[2].summary == "this is summary"
        assert result[2].pub_time == datetime(2025, 9, 2, 12, 0, tzinfo=timezone.utc)
        assert result[2].url == "http://news3.com"
        assert result[3].ticker == "TCK3"
        assert result[3].title == "News 1 for TCK3"
        assert result[3].summary == "this is summary"
        assert result[3].pub_time == datetime(2025, 9, 1, 12, 0, tzinfo=timezone.utc)
        assert result[3].url == "http://news4.com"
        assert result[4].ticker == "TCK3"
        assert result[4].title == "News 2 for TCK3"
        assert result[4].summary == "this is summary"
        assert result[4].pub_time == datetime(2025, 8, 31, 12, 0, tzinfo=timezone.utc)
        assert result[4].url == "http://news5.com"
        assert result[5].ticker == "TCK3"
        assert result[5].title == "News 3 for TCK3"
        assert result[5].summary == "this is summary"
        assert result[5].pub_time == datetime(2025, 8, 30, 12, 0, tzinfo=timezone.utc)
        assert result[5].url == "http://news6.com"

    def test__fetch_news_no_content__skips_article(self, mock_yf_ticker):
        mock_stock = MagicMock()
        mock_stock.get_news.return_value = [
            {
                "content": {
                    "title": "News 1 for TCK1",
                    "summary": "this is summary",
                    "pubDate": "2025-09-04T12:00:00Z",
                    "canonicalUrl": {"url": "http://news1.com"},
                }
            },
            {},
        ]
        mock_yf_ticker.return_value = mock_stock

        provider = YahooNewsProvider()
        result = provider.fetch_news(["TCK1"], days_behind=1)
        assert len(result) == 1
        assert result[0].ticker == "TCK1"
        assert result[0].title == "News 1 for TCK1"
        assert result[0].summary == "this is summary"
        assert result[0].pub_time == datetime(2025, 9, 4, 12, 0, tzinfo=timezone.utc)
        assert result[0].url == "http://news1.com"

    def test__fetch_news_no_articles__returns_empty_list(self, mock_yf_ticker):
        mock_stock = MagicMock()
        mock_stock.get_news.return_value = []
        mock_yf_ticker.return_value = mock_stock

        provider = YahooNewsProvider()
        result = provider.fetch_news(["TCK1"], days_behind=1)
        assert result == []

    def test__fetch_news_empty_content_fields__empty_article(self, mock_yf_ticker):
        mock_stock = MagicMock()
        mock_stock.get_news.return_value = [{"content": {"random_stuff": 123}}]
        mock_yf_ticker.return_value = mock_stock

        provider = YahooNewsProvider()
        result = provider.fetch_news(["TCK1"], days_behind=1)
        assert len(result) == 1
        assert result[0].ticker == "TCK1"
        assert result[0].title == ""
        assert result[0].summary == ""
        assert result[0].pub_time == datetime(1970, 1, 1, 0, 0, tzinfo=timezone.utc)
        assert result[0].url == ""
