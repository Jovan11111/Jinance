from abc import ABC, abstractmethod


class ReportBuilder(ABC):
    """Interface for all classes that build different parts of the report."""

    @abstractmethod
    def build_markdown(self) -> str:
        """Create .md formatted part of a report.

        Returns:
            str: Contains a part of the report in .md format.
        """
