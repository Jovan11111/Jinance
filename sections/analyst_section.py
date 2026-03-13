from managers.analyst_manager import AnalystManager
from report_building.analyst_builder import AnalystBuilder
from sections.report_section import ReportSection
from utils.enums.language import Language
from utils.localization import Localization


class AnalystSection(ReportSection):
    """Class reponsible for generating the analyst recommendations section of the report."""

    def __init__(
        self,
        provider: str,
        tickers: list[str],
        language: Language,
        number_of_companies: int,
    ):
        self.__manager = AnalystManager(provider, tickers)
        self.__builder = AnalystBuilder(Localization(language))
        self.__number_of_companies = number_of_companies

    def generate(self):
        analyst_recommendations = self.__manager.get_analyst_recommendations(
            self.__number_of_companies
        )
        return self.__builder.build_markdown(analyst_recommendations)
