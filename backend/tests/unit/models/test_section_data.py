from models.section_data import SectionData
from utils.enums.language import Language
from utils.enums.provider_type import ProviderType
from utils.enums.section_type import SectionType


class TestSectionData:
    """Test class for SectionData model."""

    def test__create_section_data__fields_have_given_values(
        self, create_section_data: SectionData
    ):
        """Check if SectionData is created correctly."""
        section_data = create_section_data
        assert section_data.type == SectionType.EARNINGS
        assert section_data.language == Language.ENGLISH
        assert section_data.provider == ProviderType.YAHOO
        assert section_data.tickers == ["TCK"]
        assert section_data.days_ahead == 1
        assert section_data.days_behind == 1
        assert section_data.number_of_companies == 1

    def test__to_dict_section_data__dict_returned_with_given_values(
        self, create_section_data: SectionData
    ):
        """Check if to_dict function returns a correct dictionary."""
        section_data = create_section_data
        assert section_data.to_dict() == {
            "type": "earnings",
            "language": "en",
            "provider": "yahoo",
            "tickers": ["TCK"],
            "days_ahead": 1,
            "days_behind": 1,
            "number_of_companies": 1,
        }
