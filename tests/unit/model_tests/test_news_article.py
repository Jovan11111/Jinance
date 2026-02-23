from datetime import datetime

from models.news_article import NewsArticle


class TestNewsArticle:
    """Test class for NewsArticle model."""

    def test__create_news_article__fields_have_given_values(self, create_news_article: NewsArticle):
        """Test that NewsArticle is created correctly."""
        article = create_news_article
        assert article.title == "title"
        assert article.summary == "summary"
        assert article.pub_time == datetime(2026, 4, 9, 12, 0, 0)
        assert article.url == "some_url"
        assert article.ticker == "TCK1"

    def test__to_dict_news_article__dict_returned_with_given_values(self, create_news_article: NewsArticle):
        """Test that to_dict returns correct dictionary."""

        article = create_news_article
        assert article.to_dict() == {
            "title": "title",
            "summary": "summary",
            "pub_time": datetime(2026, 4, 9, 12, 0, 0).isoformat(),
            "url": "some_url",
            "ticker": "TCK1",
        }
