from models.analyst_recommendation import AnalystRecommendation
from report_building.analyst_builder import AnalystBuilder
from utils.enums.language import Language
from utils.localization import Localization


class TestAnalystBuilder:
    """Test class for Analyst buidler tests."""

    def test__build_markdown_correct_data__md_string_returned(
        self, create_analyst_recommendation_dict: dict[str, list[AnalystRecommendation]]
    ):
        """Check if build markdown returns a correct md string whe regular data is given."""
        loc = Localization(Language.ENGLISH)
        analyst_builder = AnalystBuilder(loc)
        md_string = analyst_builder.build_markdown(create_analyst_recommendation_dict)

        assert loc.translate("analyst_title") in md_string
        assert loc.translate("analyst_intro") in md_string
        assert loc.translate("analyst_sells") in md_string
        assert loc.translate("analyst_buys") in md_string

    def test__build_markdown_no_data__md_string_no_table_returned(self):
        """Check if build markdown returns a string with no tables when no data is given."""
        loc = Localization(Language.ENGLISH)
        analyst_builder = AnalystBuilder(loc)
        md_string = analyst_builder.build_markdown({"buy": [], "sell": []})

        assert loc.translate("analyst_title") in md_string
        assert loc.translate("analyst_intro") in md_string
        assert loc.translate("analyst_sells") not in md_string
        assert loc.translate("analyst_buys") not in md_string
