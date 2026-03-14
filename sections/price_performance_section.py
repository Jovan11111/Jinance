import logging

from managers.price_performance_manager import PricePerformanceManager
from models.section_data import SectionData
from report_building.price_performance_builder import PricePerformanceBuilder
from sections.report_section import ReportSection
from utils.localization import Localization

logger = logging.getLogger(__name__)


class PricePerformanceSection(ReportSection):
    """Class responsible for generating the price performance section of the report."""

    def __init__(self, section_data: SectionData):
        logger.debug("PricePerformanceSection initialized.")
        self.__manager = PricePerformanceManager(
            section_data.provider, section_data.days_behind, section_data.tickers
        )
        self.__builder = PricePerformanceBuilder(Localization(section_data.language))
        self.__number_of_companies = section_data.number_of_companies

    def generate(self):
        logger.debug("Generating Price performance section of the report.")
        price_perf_data = self.__manager.get_best_worst_price_performance(
            self.__number_of_companies
        )
        return self.__builder.build_markdown(price_perf_data)
