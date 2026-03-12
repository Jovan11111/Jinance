from typing import Dict

from models.aggregated_insider_info import AggregatedInsiderInfo
from models.analyst_recommendation import AnalystRecommendation
from models.earnings_information import EarningsInformation
from models.news_article import NewsArticle
from models.price_performance_information import PricePerformanceInformation


class ReportInformation:
    """Dataclass that represents all data that is supposed to be represented on the report."""

    def __init__(
        self,
        earn_info: list[EarningsInformation],
        news: list[NewsArticle],
        price_perf: Dict[str, list[PricePerformanceInformation]],
        insiders: Dict[str, list[AggregatedInsiderInfo]],
        analysts: Dict[str, list[AnalystRecommendation]],
    ):
        self._earnings_information = earn_info
        self._news = news
        self._price_performance_information = price_perf
        self._insider_trades = insiders
        self._analyst_recommendations = analysts

    @property
    def earnings_information(self) -> list[EarningsInformation]:
        """Getter for earnings information."""
        return self._earnings_information

    @property
    def news(self) -> list[NewsArticle]:
        """Getter for news articles."""
        return self._news

    @property
    def price_performance_information(
        self,
    ) -> Dict[str, list[PricePerformanceInformation]]:
        """Getter for price performance information."""
        return self._price_performance_information

    @property
    def insider_trades(self) -> Dict[str, list[AggregatedInsiderInfo]]:
        """Getter for insider trades."""
        return self._insider_trades

    @property
    def analyst_recommendations(self) -> Dict[str, list[AnalystRecommendation]]:
        """Getter for analyst recommendations."""
        return self._analyst_recommendations

    def to_dict(self) -> dict:
        """Convert the ReportInformation object to dictionary."""
        return {
            "earnings_information": [
                earn.to_dict() for earn in self.earnings_information
            ],
            "news": [art.to_dict() for art in self.news],
            "price_performance_information": {
                "winners": [
                    price_perf.to_dict()
                    for price_perf in self.price_performance_information["winners"]
                ],
                "losers": [
                    price_perf.to_dict()
                    for price_perf in self.price_performance_information["losers"]
                ],
            },
            "insider_trades": {
                "buyers": [
                    insider.to_dict() for insider in self.insider_trades["buyers"]
                ],
                "sellers": [
                    insider.to_dict() for insider in self.insider_trades["sellers"]
                ],
            },
            "analyst_recommendations": {
                "buy": [
                    analyst.to_dict() for analyst in self.analyst_recommendations["buy"]
                ],
                "sell": [
                    analyst.to_dict()
                    for analyst in self.analyst_recommendations["sell"]
                ],
            },
        }
