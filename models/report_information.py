from models.earnings_information import EarningsInformation
from models.news_article import NewsArticle
from models.price_performance_information import PricePerformanceInformation


class ReportInformation:
    """Dataclass that represents all data that is supposed to be represented on the report."""

    def __init__(
        self,
        earn_info: list[EarningsInformation],
        news: list[NewsArticle],
        price_perf: list[PricePerformanceInformation],
    ):
        self._earnings_information = earn_info
        self._news = news
        self._price_performance_information = price_perf

    @property
    def earnings_information(self) -> list[EarningsInformation]:
        """Getter for earnings information."""
        return self._earnings_information

    @property
    def news(self) -> list[NewsArticle]:
        """Getter for news articles."""
        return self._news

    @property
    def price_performance_information(self) -> list[PricePerformanceInformation]:
        """Getter for price performance information."""
        return self._price_performance_information

    def to_dict(self) -> dict:
        """Convert the ReportInformation object to dicttionary."""
        return {
            "earnings_information": [
                earn.to_dict() for earn in self.earnings_information
            ],
            "news": [art.to_dict() for art in self.news],
            "price_performance_information": [
                performance.to_dict()
                for performance in self.price_performance_information
            ],
        }
