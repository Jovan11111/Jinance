import logging
from typing import Dict

from managers.analyst_manager import AnalystManager
from managers.earnings_manager import EarningsManager
from managers.insider_manager import InsiderManager
from managers.news_manager import NewsManager
from managers.price_performance_manager import PricePerformanceManager
from models.earnings_information import EarningsInformation
from models.news_article import NewsArticle
from models.price_performance_information import PricePerformanceInformation
from models.report_information import ReportInformation
from report_building.report_builder_director import ReportBuilderDirector
from utils.enums.language import Language
from utils.logger import setup_logging
from utils.singleton_meta import SingletonMeta

logger = logging.getLogger(__name__)


class Jinance(metaclass=SingletonMeta):
    """Main facade class of the application that manages all data, sends it to report builders."""

    def __init__(self):
        setup_logging()
        logger.debug("Jinance instance created.")
        self._earnings_manager = EarningsManager("yahoo")
        self._news_manager = NewsManager("yahoo")
        self._price_performance_manager = PricePerformanceManager("yahoo")
        self._insider_manager = InsiderManager("yahoo")
        self._analyst_manager = AnalystManager("yahoo")
        self._report_builder = ReportBuilderDirector(Language.ENGLISH)

    def generate_report(self, number_of_companies: int = 5) -> str:
        """Generates a report about all relevant information about the market.

        Args:
            number_of_companies (int, optional): Number of companies for which upcoming earnings reports are shown. Defaults to 5.

        Returns:
            str: path to a pdf file that represents generated report.
        """
        logger.debug("Generating report.")
        earnings_data: list[EarningsInformation] = (
            self._earnings_manager.get_latest_upcoming_earnings(number_of_companies)
        )

        news_data: list[NewsArticle] = self._news_manager.get_latest_news()

        price_performance_data: Dict[str, list[PricePerformanceInformation]] = (
            self._price_performance_manager.get_best_worst_price_performance(3)
        )

        insider_data = self._insider_manager.get_insider_trades(5)

        analyst_recommendations = self._analyst_manager.get_analyst_recommendations(5)

        report_info = ReportInformation(
            earn_info=earnings_data,
            news=news_data,
            price_perf=price_performance_data,
            insiders=insider_data,
            analysts=analyst_recommendations,
        )
        pdf_path = self._report_builder.create_pdf_report(report_info)

        return pdf_path
