import logging
from typing import Dict

from models.insider_information import InsiderInformation
from report_building.report_builder import ReportBuilder
from utils.localization import Localization

logger = logging.getLogger(__name__)


class InsiderBuilder(ReportBuilder):
    """Class responsible for building the part of the report that contains relevant insider information in a .md format."""

    def __init__(self, localization: Localization):
        logger.debug("InsiderBuilder initialized.")
        self.localization = localization

    def build_markdown(self, insider_data: Dict[str, list[InsiderInformation]]) -> str:
        """Returns .md formatted report part that includes all given insider information.

        Args:
            insider_data (Dict[str, list[InsiderInformation]]): Information about relevant insider transactions that needs to be represented.

        Returns:
            str: String that contains all information in a formatted way.
        """
        return ""
