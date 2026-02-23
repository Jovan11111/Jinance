from datetime import datetime
from models.earnings_information import EarningsInformation
from models.eps_information import EpsInformation
from models.news_article import NewsArticle
from models.previous_earnings_information import PreviousEarningsInformation
from models.price_performance_information import PricePerformanceInformation
from models.report_information import ReportInformation
import pytest 

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
def fixture_create_report_info(create_earn_info: EarningsInformation, create_news_article: NewsArticle, create_price_perf: PricePerformanceInformation) -> ReportInformation:
    ei1 = create_earn_info
    ei2 = create_earn_info
    na1 = create_news_article
    na2 = create_news_article
    pp1 = create_price_perf
    pp2 = create_price_perf
    return ReportInformation([ei1, ei2], [na1, na2], [pp1, pp2])
