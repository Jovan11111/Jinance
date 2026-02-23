from models.earnings_information import EarningsInformation
from models.news_article import NewsArticle
from models.price_performance_information import PricePerformanceInformation
from models.report_information import ReportInformation


class TestReportInformation:
    """Test class for ReportInformation model."""

    def test__create__report_infromation__fields_have_given_values(
        self,
        create_report_info: ReportInformation,
        create_earn_info: EarningsInformation,
        create_price_perf: PricePerformanceInformation,
        create_news_article: NewsArticle,
    ):
        """Check if ReportInformation is created correctly."""
        report_info = create_report_info
        ei = create_earn_info
        na = create_news_article
        pp = create_price_perf

        assert report_info.earnings_information == [ei, ei]
        assert report_info.news == [na, na]
        assert report_info.price_performance_information == [pp, pp]

    def test__to_dict_report_information__dict_with_given_values(
        self,
        create_report_info: ReportInformation,
        create_earn_info: EarningsInformation,
        create_price_perf: PricePerformanceInformation,
        create_news_article: NewsArticle,
    ):
        """Check if to_dict function returns correct values."""
        report_info = create_report_info
        ei = create_earn_info
        na = create_news_article
        pp = create_price_perf

        assert report_info.to_dict() == {
            "earnings_information": [ei.to_dict(), ei.to_dict()],
            "news": [na.to_dict(), na.to_dict()],
            "price_performance_information": [pp.to_dict(), pp.to_dict()],
        }
