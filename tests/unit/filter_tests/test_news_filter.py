from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock

import pytest

from filters.news_filter import NewsFilter
from models.news_article import NewsArticle


@pytest.fixture
def sample_news_articles():
    """Fixture providing 10 sample NewsArticle objects for testing."""
    now = datetime.now(timezone.utc)
    return [
        NewsArticle(
            title="Apple Reports Earnings Beat",
            summary="Apple exceeded expectations",
            pub_time=now - timedelta(days=1),
            url="https://example.com/apple1",
            ticker="AAPL",
        ),
        NewsArticle(
            title="Microsoft Announces Partnership",
            summary="New deal with Google",
            pub_time=now - timedelta(days=2),
            url="https://example.com/msft1",
            ticker="MSFT",
        ),
        NewsArticle(
            title="Tesla Stock Rises",
            summary="EV sales up",
            pub_time=now - timedelta(days=3),
            url="https://example.com/tesla1",
            ticker="TSLA",
        ),
        NewsArticle(
            title="Service Launch Announced",
            summary="Cloud service expansion",
            pub_time=now - timedelta(days=4),
            url="https://example.com/amzn1",
            ticker="AMZN",
        ),
        NewsArticle(
            title="Nvidia GPU Sales Surge",
            summary="High demand",
            pub_time=now - timedelta(days=5),
            url="https://example.com/nvda1",
            ticker="NVDA",
        ),
        NewsArticle(
            title="Old Apple Earnings Miss",
            summary="Outdated info",
            pub_time=now - timedelta(days=10),
            url="https://example.com/old1",
            ticker="AAPL",
        ),
        NewsArticle(
            title="Old Microsoft Update",
            summary="Past event",
            pub_time=now - timedelta(days=15),
            url="https://example.com/old2",
            ticker="MSFT",
        ),
        NewsArticle(
            title="TSLA Production News",
            summary="Historical",
            pub_time=now - timedelta(days=20),
            url="https://example.com/old3",
            ticker="TSLA",
        ),
        NewsArticle(
            title="Old Amazon Deal",
            summary="Old partnership",
            pub_time=now - timedelta(days=25),
            url="https://example.com/amzn1",
            ticker="AMZN",
        ),
        NewsArticle(
            title="Old Nvidia Report",
            summary="Old data",
            pub_time=now - timedelta(days=30),
            url="https://example.com/nvda1",
            ticker="NVDA",
        ),
    ]


@pytest.fixture
def mock_ai_service(mocker):
    """Fixture to mock AiService.get_instance for all tests."""
    return mocker.patch(
        "api.ai_service.AiService.get_instance", return_value=MagicMock()
    )


class TestNewsFilter:
    """Test class for NewsFilter."""

    def test__filter_by_pub_date__return_4_most_recent_news(
        self, sample_news_articles, mock_ai_service
    ):
        """Test filtering by publication date."""
        news_filter = NewsFilter()
        filtered = news_filter._filter_by_pub_date(sample_news_articles, days_behind=5)
        assert len(filtered) == 4

    def test__filter_by_seen_urls__return_8_news_with_unique_urls(
        self, sample_news_articles, mock_ai_service
    ):
        """Test filtering by seen URLs."""
        news_filter = NewsFilter()
        filtered = news_filter._filter_by_seen_urls(sample_news_articles)
        assert len(filtered) == 8

    def test__filter_by_keywords__return_4_news_with_keywords_in_title(
        self, sample_news_articles, mock_ai_service
    ):
        """Test filtering by keywords."""
        news_filter = NewsFilter()
        filtered = news_filter._filter_by_keywords(sample_news_articles)
        assert len(filtered) == 4

    def test__filter_by_ticker_in_title__return_9_news_with_ticker_in_title(
        self, sample_news_articles, mock_ai_service
    ):
        """Test filtering by ticker in title."""
        news_filter = NewsFilter()
        filtered = news_filter._filter_by_ticker_in_title(sample_news_articles)
        assert len(filtered) == 9

    def test__filter_news_integration__return_2_news_that_meet_all_criteria(
        self, sample_news_articles, mocker
    ):
        mock_ai = MagicMock()

        def fake_filter_news(articles, top_k):
            return articles[:top_k]

        mock_ai.filter_news.side_effect = fake_filter_news

        mocker.patch("filters.news_filter.AiService.get_instance", return_value=mock_ai)

        news_filter = NewsFilter()
        result = news_filter.filter_news(sample_news_articles, top_k=2, days_behind=7)

        assert result == sample_news_articles[:2]
        mock_ai.filter_news.assert_called_once()
