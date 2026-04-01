from unittest.mock import MagicMock

from providers.yahoo.yahoo_insider_provider import YahooInsiderProvider


class TestYahooInsiderProvider:
    """Test class for YahooInsiderProvider."""

    def test__fetch_insider_trades__returns_insider_information(
        self, mock_yf_ticker_insider
    ):
        """Check if calling fetch_insider_trades returns a list of InsiderInformation objects."""
        mock_stock_1 = MagicMock()
        mock_stock_2 = MagicMock()
        mock_stock_3 = MagicMock()
        mock_stock_1.get_insider_transactions.return_value.to_dict.return_value = [
            {"Value": 1000, "Text": "Purchase", "Start Date": "2023-01-01"},
            {"Value": 0, "Text": "Gift", "Start Date": "2023-02-01"},
        ]
        mock_stock_2.get_insider_transactions.return_value.to_dict.return_value = [
            {"Value": 500, "Text": "Sale", "Start Date": "2023-03-01"},
        ]
        mock_stock_3.get_insider_transactions.return_value.to_dict.return_value = []

        def ticker_side_effect(ticker):
            mapping = {
                "TCK1": mock_stock_1,
                "TCK2": mock_stock_2,
                "TCK3": mock_stock_3,
            }
            return mapping[ticker]

        mock_yf_ticker_insider.side_effect = ticker_side_effect

        provider = YahooInsiderProvider()
        result = provider.fetch_insider_trades(["TCK1", "TCK2", "TCK3"])

        assert len(result) == 3

    def test__fetch_insider_trades__no_text_field_skips_tck(
        self, mock_yf_ticker_insider
    ):
        """Check if calling fetch_insider_trades skips insider trades with empty text field."""
        mock_stock = MagicMock()
        mock_stock.get_insider_transactions.return_value.to_dict.return_value = [
            {"Value": 1000, "Text": "", "Start Date": "2023-01-01"},
            {"Value": 500, "Text": "Sale", "Start Date": "2023-03-01"},
        ]

        mock_yf_ticker_insider.return_value = mock_stock

        provider = YahooInsiderProvider()
        result = provider.fetch_insider_trades(["TCK1"])

        assert len(result) == 1

    def test__fetch_insider_trades__yahoo_exception_skips_ticker(
        self, mock_yf_ticker_insider
    ):
        """Check if calling fetch_insider_trades skips ticker when yahoo raises an exception."""
        mock_yf_ticker_insider.side_effect = Exception("Yahoo API error")

        provider = YahooInsiderProvider()
        result = provider.fetch_insider_trades(["TCK1"])

        assert len(result) == 0
