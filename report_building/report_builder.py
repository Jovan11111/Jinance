from abc import ABC, abstractmethod


class ReportBuilder(ABC):
    @abstractmethod
    def build_markdown(self) -> str:
        pass
