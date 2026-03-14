import logging
from pathlib import Path

from models.section_data import SectionData
from report_building.report_builder_director import ReportBuilderDirector
from utils.enums.language import Language
from utils.json_decoder import JsonDecoder
from utils.logger import setup_logging
from utils.singleton_meta import SingletonMeta

logger = logging.getLogger(__name__)


class Jinance(metaclass=SingletonMeta):
    """Main facade class of the application that manages all data, sends it to report builders."""

    def __init__(self):
        setup_logging()
        logger.debug("Jinance instance created.")
        self._report_builder = ReportBuilderDirector(Language.ENGLISH)

    def generate_report(self) -> str:
        """Generates a report about all relevant information about the market.

        Returns:
            str: path to a pdf file that represents generated report.
        """
        logger.debug("Generating report.")
        path_to_json_file: Path = Path(__file__).parent.joinpath("jinance_config.json")

        section_data: list[SectionData] = JsonDecoder.decode(path_to_json_file)
        pdf_path = self._report_builder.create_pdf_report(section_data)

        return pdf_path
