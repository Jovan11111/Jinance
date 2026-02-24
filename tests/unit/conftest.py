from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock

import pandas as pd
import pytest

from models.earnings_information import EarningsInformation
from models.eps_information import EpsInformation
from models.news_article import NewsArticle
from models.previous_earnings_information import PreviousEarningsInformation
from models.price_performance_information import PricePerformanceInformation
from models.report_information import ReportInformation

# --------------------------------------------------------------------------------------
# Fixtures for creating objects.
# --------------------------------------------------------------------------------------


@pytest.fixture(name="create_price_perf", scope="function")
def fixture_create_price_perf() -> PricePerformanceInformation:
    return PricePerformanceInformation(
        ticker="TCK1",
        prices=[10.0, 20.12, 12.64, 14.32, 15.01, 7.62, 8.0],
    )


@pytest.fixture(name="create_news_article", scope="function")
def fixture_create_news_article() -> NewsArticle:
    return NewsArticle(
        title="title",
        summary="summary",
        pub_time=datetime(2026, 4, 9, 12, 0, 0),
        url="some_url",
        ticker="TCK1",
    )


@pytest.fixture(name="create_prev_eps_info", scope="function")
def fixture_create_prev_eps_info() -> PreviousEarningsInformation:
    return PreviousEarningsInformation(
        expected_eps=1.5,
        actual_eps=1.4,
        price_diff=0.1,
    )


@pytest.fixture(name="create_eps_info", scope="function")
def fixture_create_eps_info() -> EpsInformation:
    return EpsInformation(avg=1.5, low=1.2, high=1.8)


@pytest.fixture(name="create_earn_info", scope="function")
def fixture_create_earn_info(create_eps_info: EpsInformation) -> EarningsInformation:
    epsi = create_eps_info
    return EarningsInformation(
        ticker="TCK",
        name="company",
        value_last_15_days=[1.2, 2.3, 3.4],
        market_cap=123456,
        eps=epsi,
        date=None,
        revenue=1234567,
        previous_earnings=[],
    )


@pytest.fixture(name="create_report_info", scope="function")
def fixture_create_report_info(
    create_earn_info: EarningsInformation,
    create_news_article: NewsArticle,
    create_price_perf: PricePerformanceInformation,
) -> ReportInformation:
    ei1 = create_earn_info
    ei2 = create_earn_info
    na1 = create_news_article
    na2 = create_news_article
    pp1 = create_price_perf
    pp2 = create_price_perf
    return ReportInformation([ei1, ei2], [na1, na2], [pp1, pp2])


# --------------------------------------------------------------------------------------
# Fixtures for creatings lists of objects.
# --------------------------------------------------------------------------------------


@pytest.fixture(name="create_earnings_info", scope="function")
def fixture_create_earnings_info() -> list[EarningsInformation]:
    earnings_information: list[EarningsInformation] = []
    base = datetime.now()
    for i in range(12):
        days = 15 - i
        dt = base + timedelta(days=days)
        idx = i + 1
        earnings_information.append(
            EarningsInformation(
                f"TCK{idx}",
                f"company{idx}",
                [],
                123456,
                EpsInformation(1, 2, 3),
                dt,
                321,
                [],
            )
        )
    return earnings_information


@pytest.fixture(name="create_news_info", scope="function")
def fixture_create_news_info() -> list[NewsArticle]:
    """Create a list of 15 news articles"""
    return [
        NewsArticle(
            f"Title {i}",
            f"Summary {i}",
            datetime(2026, 4, 9),
            f"http://example.com/article{i}",
            f"TCK{i%5}",
        )
        for i in range(15)
    ]


@pytest.fixture(name="create_price_performance_info", scope="function")
def fixture_create_price_performance_info() -> list[PricePerformanceInformation]:
    return [
        PricePerformanceInformation("TCK1", [1, 1, 1]),  # 0
        PricePerformanceInformation("TCK2", [1, 1, 2]),  # 100
        PricePerformanceInformation("TCK3", [1, 1, 3]),  # 200 # WIN
        PricePerformanceInformation("TCK4", [1, 1, 1]),  # 0
        PricePerformanceInformation("TCK5", [2, 1, 4]),  # 100
        PricePerformanceInformation("TCK6", [2, 2, 5]),  # 150
        PricePerformanceInformation("TCK7", [3, 2, 1]),  # -66.67 # LOS
        PricePerformanceInformation("TCK8", [1, 2, 1]),  # 0
        PricePerformanceInformation("TCK9", [2, 2, 1]),  # -50 # LOS
        PricePerformanceInformation("TCK10", [5, 1, 2]),  # -60 # LOS
        PricePerformanceInformation("TCK11", [1, 3, 3]),  # 200 WIN
        PricePerformanceInformation("TCK12", [1, 10, 2]),  # 100
        PricePerformanceInformation("TCK13", [3, 1, 8]),  # 166.67 # WIN
        PricePerformanceInformation("TCK14", [4, 4, 3]),  # -25
        PricePerformanceInformation("TCK15", [123, 232, 124]),  # 0.813
        PricePerformanceInformation("TCK16", [111, 222, 155]),  # 39.64
    ]


# --------------------------------------------------------------------------------------
# Fixtures for mocking providers.
# --------------------------------------------------------------------------------------


@pytest.fixture(name="mock_yahoo_earnings_provider", scope="function")
def fixture_mock_yahoo_earnings_provider(monkeypatch, create_earnings_info):
    mock_instance = MagicMock()
    mock_instance.fetch_earnings.return_value = create_earnings_info

    monkeypatch.setattr(
        "managers.earnings_manager.YahooEarningsProvider",
        lambda *args, **kwargs: mock_instance,
    )

    return mock_instance


@pytest.fixture(name="mock_yahoo_news_provider", scope="function")
def fixture_mock_yahoo_news_provider(monkeypatch, create_news_info):
    mock_instance = MagicMock()
    mock_instance.fetch_news.return_value = create_news_info
    monkeypatch.setattr(
        "managers.news_manager.YahooNewsProvider",
        lambda *args, **kwargs: mock_instance,
    )
    return mock_instance


@pytest.fixture(name="mock_yahoo_price_performance_provider", scope="function")
def fixture_mock_yahoo_price_performance_provider(
    monkeypatch, create_price_performance_info
):
    mock_instance = MagicMock()
    mock_instance.fetch_price_performance.return_value = create_price_performance_info

    monkeypatch.setattr(
        "managers.price_performance_manager.YahooPricePerformanceProvider",
        lambda *args, **kwargs: mock_instance,
    )

    return mock_instance


# --------------------------------------------------------------------------------------
# Fixtures for mocking managers.
# --------------------------------------------------------------------------------------


@pytest.fixture(name="mock_earnings_manager", scope="function")
def fixture_mock_earnings_manager(monkeypatch):
    mock_instance = MagicMock()
    mock_instance.get_latest_upcoming_earnings.return_value = []

    monkeypatch.setattr(
        "jinance.EarningsManager", lambda *args, **kwargs: mock_instance
    )

    return mock_instance


@pytest.fixture(name="mock_news_manager", scope="function")
def fixture_mock_news_manager(monkeypatch):
    mock_instance = MagicMock()
    mock_instance.get_latest_news.return_value = []

    monkeypatch.setattr("jinance.NewsManager", lambda *args, **kwargs: mock_instance)

    return mock_instance


@pytest.fixture(name="mock_price_performance_manager", scope="function")
def fixture_mock_price_performance_manager(monkeypatch):
    mock_instance = MagicMock()
    mock_instance.get_best_worst_price_performance.return_value = {}

    monkeypatch.setattr(
        "jinance.PricePerformanceManager", lambda *args, **kwargs: mock_instance
    )

    return mock_instance


# --------------------------------------------------------------------------------------
# Fixtures for mocking builders, filters, and an AI service.
# --------------------------------------------------------------------------------------


@pytest.fixture(name="mock_report_builder", scope="function")
def fixture_mock_report_builder(monkeypatch):
    mock_instance = MagicMock()
    mock_instance.create_pdf_report.return_value = "path/to/report"

    monkeypatch.setattr(
        "jinance.ReportBuilderDirector", lambda *args, **kwargs: mock_instance
    )

    return mock_instance


@pytest.fixture(name="mock_graph_builder", scope="function")
def fixture_mock_graph_builder(monkeypatch):
    mock_instance = MagicMock()
    mock_instance.build_price_graph.return_value = "path/to/graph"

    monkeypatch.setattr(
        "report_building.earnings_buidler.GraphBuilder",
        lambda *args, **kwargs: mock_instance,
    )

    return mock_instance


# --------------------------------------------------------------------------------------
# Fixtures for ai service and filters
# --------------------------------------------------------------------------------------


@pytest.fixture(name="mock_ai_service", scope="function")
def fixture_mock_ai_service(mocker):
    """Fixture to mock AiService.get_instance for all tests."""
    return mocker.patch(
        "api.ai_service.AiService.get_instance", return_value=MagicMock()
    )


@pytest.fixture(name="mock_yahoo_news_filter", scope="function", autouse=True)
def fixture_mock_yahoo_news_filter(monkeypatch, create_news_info):
    mock_instance = MagicMock()
    mock_instance.filter_news.return_value = create_news_info[:5]
    monkeypatch.setattr(
        "managers.news_manager.NewsFilter",
        lambda *args, **kwargs: mock_instance,
    )
    return mock_instance


@pytest.fixture(name="sample_news_articles", scope="function")
def fixture_sample_news_articles():
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


# --------------------------------------------------------------------------------------
# Fixtures for mocking yf API classes
# --------------------------------------------------------------------------------------


@pytest.fixture(name="mock_yf_ticker_news", scope="function")
def fixture_mock_yf_ticker_news(mocker):
    return mocker.patch("providers.yahoo.yahoo_news_provider.yf.Ticker")


@pytest.fixture(name="mock_yf_ticker_price_performance", scope="function")
def fixture_mock_yf_ticker_price_performance(mocker):
    return mocker.patch("providers.yahoo.yahoo_price_performance_provider.yf.Ticker")


@pytest.fixture(name="mock_yf_ticker_earnings", scope="function")
def fixture_mock_yf_ticker_earnings(mocker):
    return mocker.patch("providers.yahoo.yahoo_earnings_provider.yf.Ticker")


@pytest.fixture(name="yf_stock_factory", scope="function")
def fixture_yf_stock_factory():
    """
    Use like this:
        stock = yf_stock_factory(
            calendar={"Earnings Date": [pd.Timestamp("2026-04-01")]},
            info={"shortName": "Acme", "marketCap": 12345},
            history_15d_df=pd.DataFrame({"Close": [1.0, 2.0, 3.0]}),
            history_range_df=pd.DataFrame({"Close": [10.0, 12.0]}),
            earnings_dates_df=pd.DataFrame(
                {"EPS Estimate": [1.1], "Reported EPS": [1.0]},
                index=[pd.Timestamp("2026-01-01")],
            ),
        )
    """

    def _factory(
        *,
        calendar=None,
        info=None,
        history_15d=None,
        history_range=None,
        earnings_dates=None,
    ):
        stock = MagicMock()

        cal = calendar or {}
        if "Earnings Date" in cal and cal["Earnings Date"] is not None:
            normalized = []
            for v in cal["Earnings Date"]:
                try:
                    normalized.append(v.date())
                except Exception:
                    normalized.append(v)
            cal["Earnings Date"] = normalized
        stock.calendar = cal

        if isinstance(info, MagicMock):
            stock.info = info
        else:
            stock.info = info or {}

        if history_15d is None:
            hist15 = pd.DataFrame()
        elif isinstance(history_15d, pd.DataFrame):
            hist15 = history_15d
        else:
            hist15 = pd.DataFrame(history_15d)

        if history_range is None:
            histr = pd.DataFrame()
        elif isinstance(history_range, pd.DataFrame):
            histr = history_range
        else:
            histr = pd.DataFrame(history_range)

        if earnings_dates is None:
            edf = pd.DataFrame()
        elif isinstance(earnings_dates, pd.DataFrame):
            edf = earnings_dates
        else:
            edf = pd.DataFrame(earnings_dates)
            if edf.index.dtype == "int64" or edf.index.empty:
                idx = [
                    pd.Timestamp(datetime.now() - timedelta(days=60 * (i + 1)))
                    for i in range(len(edf))
                ]
                edf.index = pd.DatetimeIndex(idx)

        def history_side_effect(*args, **kwargs):
            if kwargs.get("period") == "15d":
                return hist15
            return histr

        stock.history.side_effect = history_side_effect
        stock.get_earnings_dates.return_value = edf
        return stock

    return _factory
