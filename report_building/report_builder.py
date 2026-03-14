from abc import ABC, abstractmethod

from utils.localization import Localization


class ReportBuilder(ABC):
    """Interface for all classes that build different parts of the report."""

    def __init__(self, localization: Localization):
        self._localization = localization

    @abstractmethod
    def build_markdown(self) -> str:
        """Create .md formatted part of a report.

        Returns:
            str: Contains a part of the report in .md format.
        """
