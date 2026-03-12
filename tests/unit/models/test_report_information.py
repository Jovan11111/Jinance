from typing import Dict

from models.aggregated_insider_info import AggregatedInsiderInfo
from models.analyst_recommendation import AnalystRecommendation
from models.earnings_information import EarningsInformation
from models.news_article import NewsArticle
from models.price_performance_information import PricePerformanceInformation
from models.report_information import ReportInformation


class TestReportInformation:
    """Test class for ReportInformation model."""

    def test__create__report_information__fields_have_given_values(
        self,
        create_report_info: ReportInformation,
        create_earn_info: EarningsInformation,
        create_price_perf_dict: Dict[str, list[PricePerformanceInformation]],
        create_news_article: NewsArticle,
        create_aggregated_insider_information_dict: AggregatedInsiderInfo,
        create_analyst_recommendation_dict: AnalystRecommendation,
    ):
        """Check if ReportInformation is created correctly."""
        report_info = create_report_info
        ei = create_earn_info
        pp = create_price_perf_dict
        na = create_news_article
        ai = create_aggregated_insider_information_dict
        ar = create_analyst_recommendation_dict

        assert report_info.earnings_information == [ei, ei]
        assert report_info.news == [na, na]
        assert report_info.price_performance_information == pp
        assert report_info.insider_trades == ai
        assert report_info.analyst_recommendations == ar

    def test__to_dict_report_information__dict_with_given_values(
        self,
        create_report_info: ReportInformation,
        create_earn_info: EarningsInformation,
        create_price_perf_dict: Dict[str, list[PricePerformanceInformation]],
        create_news_article: NewsArticle,
        create_aggregated_insider_information_dict: AggregatedInsiderInfo,
        create_analyst_recommendation_dict: AnalystRecommendation,
    ):
        """Check if to_dict function returns correct values."""
        report_info = create_report_info
        ei = create_earn_info
        na = create_news_article
        pp = create_price_perf_dict
        ai = create_aggregated_insider_information_dict
        ar = create_analyst_recommendation_dict

        assert report_info.to_dict() == {
            "earnings_information": [ei.to_dict(), ei.to_dict()],
            "news": [na.to_dict(), na.to_dict()],
            "price_performance_information": {
                "winners": [p.to_dict() for p in pp["winners"]],
                "losers": [p.to_dict() for p in pp["losers"]],
            },
            "insider_trades": {
                "buyers": [a.to_dict() for a in ai["buyers"]],
                "sellers": [a.to_dict() for a in ai["sellers"]],
            },
            "analyst_recommendations": {
                "buy": [a.to_dict() for a in ar["buy"]],
                "sell": [a.to_dict() for a in ar["sell"]],
            },
        }
