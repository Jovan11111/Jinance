from data_collection.earnings_manager import EarningsManager
from report_building.report_builder import ReportBuilder
from utils.singleton_meta import SingletonMeta


class Jinance(metaclass=SingletonMeta):
    def __init__(self):
        print("Jinance initialized")
        self.earnings_manager: EarningsManager = EarningsManager.get_instance()
        self.report_builder: ReportBuilder = ReportBuilder.get_instance()

    def generate_report(self, number_of_companies: int = 5) -> str:

        earnings_data = self.earnings_manager.get_latest_upcoming_earnings(
            number_of_companies
        )

        pdf_path = self.report_builder.create_pdf_report(earnings_data)

        return pdf_path
