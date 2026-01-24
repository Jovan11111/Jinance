from datetime import datetime

from models.news_article import NewsArticle


class TestNewsArticle:
    """Test class for NewsArticle model."""

    def test__create_news_article__fields_have_given_values(self):
        """Test that NewsArticle is created correctly."""
        pub_time = datetime(2026, 4, 9, 12, 0, 0)
        article = NewsArticle(
            title="title",
            summary="summary",
            pub_time=pub_time,
            url="some_url",
            ticker="some_ticker",
        )
        assert article.title == "title"
        assert article.summary == "summary"
        assert article.pub_time == pub_time
        assert article.url == "some_url"
        assert article.ticker == "some_ticker"

    def test__to_dict_news_article__dict_returned_with_given_values(self):
        """Test that to_dict returns correct dictionary."""

        pub_time = datetime(2026, 4, 9, 12, 0, 0)
        article = NewsArticle(
            title="title",
            summary="summary",
            pub_time=pub_time,
            url="some_url",
            ticker="some_ticker",
        )
        assert article.to_dict() == {
            "title": "title",
            "summary": "summary",
            "pub_time": pub_time.isoformat(),
            "url": "some_url",
            "ticker": "some_ticker",
        }
