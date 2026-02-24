from managers.news_manager import NewsManager
from providers.yahoo.yahoo_news_provider import YahooNewsProvider
from utils import constants


class TestNewsManager:
    """Test class for News manager tests."""

    def test__initialize_news_manager__all_fields_correct(self):
        """Check if initializiting manager with reasonable values creates News manager correctly."""
        news_manager = NewsManager("yahoo", 5, constants.TICKERS_SP_20)

        assert news_manager.days_behind == 5
        assert news_manager.tickers == constants.TICKERS_SP_20
        assert isinstance(news_manager.provider, YahooNewsProvider)

    def test__initialize_news_manager_negative_days_behind__initialized_with_default_days_begind(
        self,
    ):
        """Check if initializing manager with negative days_behind initializes it with default value."""
        news_manager = NewsManager("yahoo", -5, constants.TICKERS_SP_20)

        assert news_manager.days_behind == 1
        assert news_manager.tickers == constants.TICKERS_SP_20
        assert isinstance(news_manager.provider, YahooNewsProvider)

    def test__initialize_news_manager_default_values__initialized_with_default_values(
        self,
    ):
        """Check if initializing manager with default values initializes it with default values."""
        news_manager = NewsManager()

        assert news_manager.days_behind == 1
        assert news_manager.tickers == constants.TICKERS_SP_100
        assert isinstance(news_manager.provider, YahooNewsProvider)

    def test__initialize_news_manager_non_existant_provider__initialized_with_default_provider(
        self,
    ):
        """Check if initializing manager with non existant provider initializes it with default provider."""
        news_manager = NewsManager("NON_EXISTANT", 1, constants.TICKERS_SP_50)

        assert news_manager.days_behind == 1
        assert news_manager.tickers == constants.TICKERS_SP_50
        assert isinstance(news_manager.provider, YahooNewsProvider)

    def test__get_latest_news__returns_sorted_and_filtered_news(
        self, mock_yahoo_news_provider, mock_yahoo_news_filter, create_news_info
    ):
        """Check if get_latest_news returns sorted and filtered news."""
        news_manager = NewsManager()
        result = news_manager.get_latest_news()
        assert result == create_news_info[:5]
