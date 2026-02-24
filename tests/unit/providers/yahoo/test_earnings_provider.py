from datetime import datetime, timedelta
from unittest.mock import MagicMock, PropertyMock

from providers.yahoo.yahoo_earnings_provider import YahooEarningsProvider


class TestEearningsProvider:
    def test__fetch_earnings_multiple_tickers__return_earnings_list(
        self, mock_yf_ticker_earnings, yf_stock_factory
    ):
        cutoff = (datetime.now() + timedelta(days=30)).date()
        now = datetime.now()

        stock_1 = yf_stock_factory(
            calendar={
                "Earnings Date": [(now + timedelta(days=5)).date()],
                "Earnings Average": 1.23,
                "Earnings Low": 1.12,
                "Earnings High": 1.32,
                "Revenue Average": 123456,
            },
            info={"shortName": "company 1", "marketCap": 10000000},
            history_15d={"Close": [100.0, 101.5, 102.3]},
            history_range={"Close": [95.0, 105.0]},
            earnings_dates={"EPS Estimate": [1.1], "Reported EPS": [1.05]},
        )
        stock_2 = yf_stock_factory(
            calendar={
                "Earnings Date": [(now + timedelta(days=10)).date()],
                "Earnings Average": 2.34,
                "Earnings Low": 2.20,
                "Earnings High": 2.50,
                "Revenue Average": 654321,
            },
            info={"shortName": "company 2", "marketCap": 20000000},
            history_15d={"Close": [200.0, 202.5, 205.3]},
            history_range={"Close": [190.0, 210.0]},
            earnings_dates={"EPS Estimate": [2.3], "Reported EPS": [2.5]},
        )
        stock_3 = yf_stock_factory(
            calendar={
                "Earnings Date": [(now + timedelta(days=20)).date()],
                "Earnings Average": 3.45,
                "Earnings Low": 3.30,
                "Earnings High": 3.60,
                "Revenue Average": 987654,
            },
            info={"shortName": "company 3", "marketCap": 30000000},
            history_15d={"Close": [300.0, 303.5, 305.3]},
            history_range={"Close": [290.0, 310.0]},
            earnings_dates={"EPS Estimate": [3.4], "Reported EPS": [3.6]},
        )

        def ticker_side_effect(ticker):
            mapping = {"TCK1": stock_1, "TCK2": stock_2, "TCK3": stock_3}
            return mapping[ticker]

        mock_yf_ticker_earnings.side_effect = ticker_side_effect
        provider = YahooEarningsProvider()
        result = provider.fetch_earnings(["TCK1", "TCK2", "TCK3"], cutoff)

        assert len(result) == 3
        tck1 = result[0]
        tck2 = result[1]
        tck3 = result[2]
        assert tck1.ticker == "TCK1"
        assert tck1.name == "company 1"
        assert tck1.market_cap == 10000000
        assert tck1.value_last_15_days == [100.0, 101.5, 102.3]

        assert tck2.ticker == "TCK2"
        assert tck2.name == "company 2"
        assert tck2.market_cap == 20000000
        assert tck2.value_last_15_days == [200.0, 202.5, 205.3]

        assert tck3.ticker == "TCK3"
        assert tck3.name == "company 3"
        assert tck3.market_cap == 30000000
        assert tck3.value_last_15_days == [300.0, 303.5, 305.3]

    def test__fetch_earnings_no_calendar__calendar_exception_skips(
        self, mock_yf_ticker_earnings
    ):
        cutoff = (datetime.now() + timedelta(days=30)).date()
        stock = MagicMock()
        type(stock).calendar = PropertyMock(
            side_effect=Exception("calendar unavailable")
        )

        mock_yf_ticker_earnings.return_value = stock

        provider = YahooEarningsProvider()
        result = provider.fetch_earnings(["TCK1"], cutoff)

        assert result == []

    def test__fetch_earnings_date_out_of_range__empty_list(
        self, mock_yf_ticker_earnings
    ):
        cutoff = (datetime.now() + timedelta(days=30)).date()
        stock = MagicMock()
        type(stock).calendar = PropertyMock(
            return_value={"Earnings Date": [cutoff + timedelta(days=1)]}
        )

        mock_yf_ticker_earnings.return_value = stock

        provider = YahooEarningsProvider()
        result = provider.fetch_earnings(["TCK1"], cutoff)

        assert result == []

    def test__fetch_earnings_earnings_date_exception__skips(
        self, mock_yf_ticker_earnings, yf_stock_factory
    ):
        cutoff = (datetime.now() + timedelta(days=30)).date()
        stock = MagicMock()
        stock.calendar = MagicMock()
        stock.calendar.get = MagicMock(
            side_effect=Exception("earnings date unavailable")
        )

        mock_yf_ticker_earnings.return_value = stock

        provider = YahooEarningsProvider()
        result = provider.fetch_earnings(["TCK1"], cutoff)

        assert result == []

    def test__fetch_earnings_info_exception__market_cap_company_nameempty(
        self, mock_yf_ticker_earnings, yf_stock_factory
    ):
        cutoff = (datetime.now() + timedelta(days=30)).date()
        stock_1 = yf_stock_factory(
            calendar={
                "Earnings Date": [(datetime.now() + timedelta(days=5)).date()],
                "Earnings Average": 1.23,
                "Earnings Low": 1.12,
                "Earnings High": 1.32,
                "Revenue Average": 123456,
            },
            info=MagicMock(
                get=MagicMock(side_effect=Exception("stock info unavailable"))
            ),
            history_15d={"Close": [100.0, 101.5, 102.3]},
            history_range={"Close": [95.0, 105.0]},
            earnings_dates={"EPS Estimate": [1.1], "Reported EPS": [1.05]},
        )

        def ticker_side_effect(ticker):
            mapping = {"TCK1": stock_1}
            return mapping[ticker]

        mock_yf_ticker_earnings.side_effect = ticker_side_effect

        provider = YahooEarningsProvider()
        result = provider.fetch_earnings(["TCK1"], cutoff)

        assert len(result) == 1
        assert result[0].ticker == "TCK1"
        assert result[0].name == ""
        assert result[0].market_cap == 0
        assert result[0].value_last_15_days == [100.0, 101.5, 102.3]
