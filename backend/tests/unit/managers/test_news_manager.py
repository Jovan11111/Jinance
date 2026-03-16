from managers.news_manager import NewsManager


class TestNewsManager:
    """Test class for News manager tests."""

    def test__get_latest_news__returns_sorted_and_filtered_news(
        self, mock_yahoo_news_provider, mock_yahoo_news_filter, create_news_info
    ):
        """Check if get_latest_news returns sorted and filtered news."""
        news_manager = NewsManager()
        result = news_manager.get_latest_news(5)
        assert result == create_news_info[:5]

    def test__get_latest_news_negative_articles__returns_sorted_and_filtered_news(
        self, mock_yahoo_news_provider, mock_yahoo_news_filter, create_news_info
    ):
        """Check if get_latest_news with negative number_of_articles defaults it to 10 and returns sorted and filtered news."""
        news_manager = NewsManager()
        result = news_manager.get_latest_news(-5)
        assert result == create_news_info[:5]

    def test__get_latest_news_non_existent_provider__returns_sorted_and_filtered_news(
        self, mock_yahoo_news_provider, mock_yahoo_news_filter, create_news_info
    ):
        """Check if get_latest_news with non existent provider defaults it to yahoo and returns sorted and filtered news."""
        news_manager = NewsManager(provider="NON_EXISTENT")
        result = news_manager.get_latest_news(5)
        assert result == create_news_info[:5]
