from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock

import pytest

from filters.news_filter import NewsFilter
from models.news_article import NewsArticle


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
