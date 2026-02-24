from unittest.mock import MagicMock

import pytest

from providers.yahoo.yahoo_price_performance_provider import (
    YahooPricePerformanceProvider,
)





class TestPricePerformanceProvider:
    def test_fetch_price_performance__multiple_tickers(self, mock_yf_ticker):
        mock_stock_1 = MagicMock()
        mock_stock_2 = MagicMock()
        mock_stock_3 = MagicMock()

        def make_mock_hist(prices):
            m = MagicMock()
            m.empty = False
            m.__getitem__.return_value.round.return_value.tolist.return_value = prices
            return m

        mock_stock_1.history.return_value = make_mock_hist([31.123, 54.321, 67.899])
        mock_stock_2.history.return_value = make_mock_hist([200.00, 198.13, 205.321])
        mock_stock_3.history.return_value = make_mock_hist([50.321, 52.517, 54.037])

        def ticker_side_effect(ticker):
            mapping = {"TCK1": mock_stock_1, "TCK2": mock_stock_2, "TCK3": mock_stock_3}
            return mapping[ticker]

        mock_yf_ticker.side_effect = ticker_side_effect

        provider = YahooPricePerformanceProvider()
        result = provider.fetch_price_performance(
            ["TCK1", "TCK2", "TCK3"], days_behind=180
        )

        assert len(result) == 3
        assert result[0].ticker == "TCK1"
        assert result[0].prices == [31.123, 54.321, 67.899]
        assert result[1].ticker == "TCK2"
        assert result[1].prices == [200.00, 198.13, 205.321]
        assert result[2].ticker == "TCK3"
        assert result[2].prices == [50.321, 52.517, 54.037]

    def test_fetch_price_performance__empty_history_returns_empty_list(
        self, mock_yf_ticker
    ):
        mock_stock = MagicMock()

        mock_hist = MagicMock()
        mock_hist.empty = True
        mock_stock.history.return_value = mock_hist

        mock_yf_ticker.return_value = mock_stock

        provider = YahooPricePerformanceProvider()
        result = provider.fetch_price_performance(["TCK1"], days_behind=10)

        assert result == []

    def test_fetch_price_performance__yahoo_exception_skips_ticker(
        self, mock_yf_ticker
    ):
        mock_yf_ticker.side_effect = Exception("Yahoo API error")

        provider = YahooPricePerformanceProvider()
        result = provider.fetch_price_performance(["TCK1"], days_behind=10)

        assert result == []
