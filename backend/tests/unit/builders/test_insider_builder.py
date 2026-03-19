from models.aggregated_insider_info import AggregatedInsiderInfo
from report_building.insider_builder import InsiderBuilder
from utils.enums.language import Language
from utils.localization import Localization


class TestInsiderBuilder:
    """Test class for Insider builder tests."""

    def test__build_markdown_correct_data__md_string_returned(
        self,
        create_aggregated_insider_information_dict: dict[
            str, list[AggregatedInsiderInfo]
        ],
    ):
        """Check if build markdown returns a correct full md string when correct data is sent."""
        loc = Localization(Language.ENGLISH)
        insider_builder = InsiderBuilder(loc)
        md_string = insider_builder.build_markdown(
            create_aggregated_insider_information_dict
        )

        assert loc.translate("insider_title") in md_string
        assert loc.translate("insider_intro") in md_string
        assert loc.translate("insider_sellers") in md_string
        assert loc.translate("insider_buyers") in md_string

    def test__build_markdown_no_data__md_string_no_tables(self):
        """Check if build markdown returns a md string with no tables when no data is given."""
        loc = Localization(Language.ENGLISH)
        insider_builder = InsiderBuilder(loc)
        md_string = insider_builder.build_markdown({"buyers": [], "sellers": []})

        assert loc.translate("insider_title") in md_string
        assert loc.translate("insider_intro") in md_string
        assert loc.translate("insider_sellers") not in md_string
        assert loc.translate("insider_buyers") not in md_string
