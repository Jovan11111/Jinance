from managers.price_performance_manager import PricePerformanceManager
from report_building.price_performance_builder import PricePerformanceBuilder
from sections.report_section import ReportSection
from utils.enums.language import Language
from utils.localization import Localization


class PricePerformanceSection(ReportSection):
    """Class responsible for generating the price performance section of the report."""

    def __init__(
        self,
        provider: str,
        days_behind: int,
        tickers: list[str],
        language: Language,
        number_of_companies: int,
    ):
        self.__manager = PricePerformanceManager(provider, days_behind, tickers)
        self.__builder = PricePerformanceBuilder(Localization(language))
        self.__number_of_companies = number_of_companies

    def generate(self):
        price_perf_data = self.__manager.get_best_worst_price_performance(
            self.__number_of_companies
        )
        return self.__builder.build_markdown(price_perf_data)
