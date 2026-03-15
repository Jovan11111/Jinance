from typing import Any, Optional

from utils.enums.language import Language
from utils.enums.provider_type import ProviderType
from utils.enums.section_type import SectionType


class SectionData:
    """Class that represents a data model sent to each section to instantiate managers and builders with correct parameters.

    Fields:
        type (SectionType): Type of the section that is being instantiated.
        language (Language): Language in which that part of the report is generated in.
        provider (ProviderType): Type of provider for data shown in the report.
        tickers (list[str]): Lits of ticker from which to retrieve data for that part of the report.
        days_ahead (Optional[int]): How far into the future the manager should look. Optional since some managers don't have this.
        days_behind (Optional[int]): How far into the past the manager should look. Optional since some managers don't have this.
        number_of_companies (int): Number of companies/articles that should be shown in that part of the report.
    """

    def __init__(
        self,
        type: SectionType,
        language: Language,
        provider: ProviderType,
        tickers: list[str],
        days_ahead: Optional[int],
        days_behind: Optional[int],
        number_of_companies: int,
    ):
        self.__type: SectionType = type
        self.__language: Language = language
        self.__provider: ProviderType = provider
        self.__tickers: list[str] = tickers
        self.__days_ahead: Optional[int] = days_ahead
        self.__days_behind: Optional[int] = days_behind
        self.__number_of_companies: int = number_of_companies

    @property
    def type(self) -> SectionType:
        """Getter for type"""
        return self.__type

    @property
    def language(self) -> Language:
        """Getter for language"""
        return self.__language

    @property
    def provider(self) -> ProviderType:
        """Getter for provider"""
        return self.__provider

    @property
    def tickers(self) -> list[str]:
        """Getter for tickers"""
        return self.__tickers

    @property
    def days_ahead(self) -> Optional[int]:
        """Getter for days_ahead"""
        return self.__days_ahead

    @property
    def days_behind(self) -> Optional[int]:
        """Getter for days_behind"""
        return self.__days_behind

    @property
    def number_of_companies(self) -> int:
        """Getter for number_of_companies"""
        return self.__number_of_companies

    def to_dict(self) -> dict[str, Any]:
        """Get SectionData class object in dict format."""
        return {
            "type": self.type,
            "language": self.language,
            "provider": self.provider,
            "tickers": self.tickers,
            "days_ahead": self.days_ahead,
            "days_behind": self.days_behind,
            "number_of_companies": self.number_of_companies,
        }
