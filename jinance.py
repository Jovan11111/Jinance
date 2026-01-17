from managers.earnings_manager import EarningsManager
from managers.news_manager import NewsManager
from models.earnings_information import EarningsInformation
from models.news_article import NewsArticle
from report_building.report_builder_director import ReportBuilderDirector
from utils.singleton_meta import SingletonMeta


class Jinance(metaclass=SingletonMeta):
    def __init__(self):
        self._earnings_manager = EarningsManager("yahoo")
        self._news_manager = NewsManager("yahoo")
        self._report_builder = ReportBuilderDirector()

    @property
    def earnings_manager(self) -> EarningsManager:
        return self._earnings_manager

    @property
    def report_builder(self) -> ReportBuilderDirector:
        return self._report_builder

    @property
    def news_manager(self) -> NewsManager:
        return self._news_manager

    def generate_report(self, number_of_companies: int = 5) -> str:

        earnings_data: list[EarningsInformation] = (
            self.earnings_manager.get_latest_upcoming_earnings(number_of_companies)
        )

        news_data: list[NewsArticle] = self.news_manager.get_latest_news()

        pdf_path = self.report_builder.create_pdf_report(earnings_data, news_data)

        return pdf_path
