from managers.analyst_manager import AnalystManager
from models.section_data import SectionData
from report_building.analyst_builder import AnalystBuilder
from sections.report_section import ReportSection
from utils.localization import Localization


class AnalystSection(ReportSection):
    """Class reponsible for generating the analyst recommendations section of the report."""

    def __init__(self, section_data: SectionData):
        self.__manager = AnalystManager(section_data.provider, section_data.tickers)
        self.__builder = AnalystBuilder(Localization(section_data.language))
        self.__number_of_companies = section_data.number_of_companies

    def generate(self):
        analyst_recommendations = self.__manager.get_analyst_recommendations(
            self.__number_of_companies
        )
        return self.__builder.build_markdown(analyst_recommendations)
