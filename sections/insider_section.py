from managers.insider_manager import InsiderManager
from models.section_data import SectionData
from report_building.insider_builder import InsiderBuilder
from sections.report_section import ReportSection
from utils.localization import Localization


class InsiderSection(ReportSection):
    """Class responsible for generating the insider trading section of the report."""

    def __init__(self, section_data: SectionData):
        self.__manager = InsiderManager(
            section_data.provider, section_data.days_behind, section_data.tickers
        )
        self.__builder = InsiderBuilder(Localization(section_data.language))
        self.__number_of_companies = section_data.number_of_companies

    def generate(self):
        insider_data = self.__manager.get_insider_trades(self.__number_of_companies)
        return self.__builder.build_markdown(insider_data)
