from abc import ABC, abstractmethod


class ReportSection(ABC):
    """Interface for all classes that represent a section of a report."""

    @abstractmethod
    def generate(self) -> str:
        """Generate a part of the report

        Method that generates a part of the report based on which part is supposed to be generated.
        Uses manager to get the data and builder to generate the .md text.
        Returns:
            str: content of the report in .md format.
        """
