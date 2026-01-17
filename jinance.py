from managers.earnings_manager import EarningsManager
from managers.news_manager import NewsManager
from models.earnings_information import EarningsInformation
from models.news_article import NewsArticle
from report_building.report_builder_director import ReportBuilderDirector
from utils.singleton_meta import SingletonMeta


class Jinance(metaclass=SingletonMeta):
    """Main facade class of the aplication that manages all data, sends it to report builders."""

    def __init__(self):
        self._earnings_manager = EarningsManager("yahoo")
        self._news_manager = NewsManager("yahoo")
        self._report_builder = ReportBuilderDirector()

    def generate_report(self, number_of_companies: int = 5) -> str:
        """Generates a report about all relevant information about the market.

        Args:
            number_of_companies (int, optional): Number of companies for which upcoming earnings reports are shown. Defaults to 5.

        Returns:
            str: path to a pdf file that represents generated report.
        """
        earnings_data: list[EarningsInformation] = (
            self.earnings_manager.get_latest_upcoming_earnings(number_of_companies)
        )

        news_data: list[NewsArticle] = self.news_manager.get_latest_news()

        pdf_path = self.report_builder.create_pdf_report(earnings_data, news_data)

        return pdf_path
