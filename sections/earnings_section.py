from managers.earnings_manager import EarningsManager
from models.section_data import SectionData
from report_building.earnings_builder import EarningsBuilder
from sections.report_section import ReportSection
from utils.localization import Localization


class EarningsSection(ReportSection):
    """Class responsible for generating the earnings section of the report."""

    def __init__(self, section_data: SectionData):
        self.__manager = EarningsManager(
            section_data.provider, section_data.days_ahead, section_data.tickers
        )
        self.__builder = EarningsBuilder(Localization(section_data.language))
        self.__number_of_companies = section_data.number_of_companies

    def generate(self) -> str:
        earnings_data = self.__manager.get_latest_upcoming_earnings(
            self.__number_of_companies
        )
        return self.__builder.build_markdown(earnings_data)
