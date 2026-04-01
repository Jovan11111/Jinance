from unittest.mock import MagicMock

from providers.yahoo.yahoo_analyst_provider import YahooAnalystProvider


class TestYahooAnalystProvider:
    """Test class for YahooAnalystProvider."""

    def test__fetch_analyst_ratings__returns_analyst_recommendations(
        self, mock_yf_ticker_analyst
    ):
        """Check if calling fetch_analyst_recommendations returns a list of AnalystRecommendation objects."""
        mock_stock_1 = MagicMock()
        mock_stock_2 = MagicMock()
        mock_stock_3 = MagicMock()
        mock_stock_4 = MagicMock()
        mock_stock_1.info.get.return_value = 1.0
        mock_stock_2.info.get.return_value = 2.3
        mock_stock_3.info.get.return_value = 1.3
        mock_stock_4.info.get.return_value = 4.2

        def ticker_side_effect(ticker):
            mapping = {
                "TCK1": mock_stock_1,
                "TCK2": mock_stock_2,
                "TCK3": mock_stock_3,
                "TCK4": mock_stock_4,
            }
            return mapping[ticker]

        mock_yf_ticker_analyst.side_effect = ticker_side_effect

        provider = YahooAnalystProvider()
        result = provider.fetch_analyst_recommendations(
            ["TCK1", "TCK2", "TCK3", "TCK4"]
        )

        assert len(result) == 4

    def test__fetch_analyst_ratings__invalid_mean_value_skips_ticker(
        self, mock_yf_ticker_analyst
    ):
        """Check if calling fetch_analyst_recommendations with invalid mean value skips the ticker."""
        mock_stock_1 = MagicMock()
        mock_stock_2 = MagicMock()
        mock_stock_3 = MagicMock()
        mock_stock_1.info.get.return_value = 0.5
        mock_stock_2.info.get.return_value = 6.0
        mock_stock_3.info.get.return_value = 3.0

        def ticker_side_effect(ticker):
            mapping = {
                "TCK1": mock_stock_1,
                "TCK2": mock_stock_2,
                "TCK3": mock_stock_3,
            }
            return mapping[ticker]

        mock_yf_ticker_analyst.side_effect = ticker_side_effect
        provider = YahooAnalystProvider()
        result = provider.fetch_analyst_recommendations(["TCK1", "TCK2", "TCK3"])

        assert len(result) == 1

    def test__fetch_analyst_ratings__yahoo_exception_skips_ticker(
        self, mock_yf_ticker_analyst
    ):
        """Check if calling fetch_analyst_recommendations skips ticker when yahoo raises an exception."""
        mock_stock_2 = MagicMock()
        mock_stock_2.info.get.return_value = 2.0

        def ticker_side_effect(ticker):
            mapping = {
                "TCK1": Exception("Yahoo API error"),
                "TCK2": mock_stock_2,
            }
            value = mapping[ticker]
            if isinstance(value, Exception):
                raise value
            return value

        mock_yf_ticker_analyst.side_effect = ticker_side_effect
        provider = YahooAnalystProvider()
        result = provider.fetch_analyst_recommendations(["TCK1", "TCK2"])

        assert len(result) == 1
