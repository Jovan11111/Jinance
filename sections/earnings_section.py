from managers.earnings_manager import EarningsManager
from report_building.earnings_builder import EarningsBuilder
from sections.report_section import ReportSection
from utils.enums.language import Language
from utils.localization import Localization


class EarningsSection(ReportSection):
    """Class responsible for generating the earnings section of the report."""

    def __init__(
        self,
        provider: str,
        days_ahead: int,
        tickers: list[str],
        language: Language,
        number_of_companies: int,
    ):
        self.__manager = EarningsManager(provider, days_ahead, tickers)
        self.__builder = EarningsBuilder(Localization(language))
        self.__number_of_companies = number_of_companies

    def generate(self) -> str:
        earnings_data = self.__manager.get_latest_upcoming_earnings(
            self.__number_of_companies
        )
        return self.__builder.build_markdown(earnings_data)
