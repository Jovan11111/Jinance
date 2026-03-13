from managers.insider_manager import InsiderManager
from report_building.insider_builder import InsiderBuilder
from sections.report_section import ReportSection
from utils.enums.language import Language
from utils.localization import Localization


class InsiderSection(ReportSection):
    """Class responsible for generating the insider trading section of the report."""

    def __init__(
        self,
        provider: str,
        days_behind: int,
        tickers: list[str],
        language: Language,
        number_of_companies: int,
    ):
        self.__manager = InsiderManager(provider, days_behind, tickers)
        self.__builder = InsiderBuilder(Localization(language))
        self.__number_of_companies = number_of_companies

    def generate(self):
        insider_data = self.__manager.get_insider_trades(self.__number_of_companies)
        return self.__builder.build_markdown(insider_data)
