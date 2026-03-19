from datetime import datetime

from models.earnings_information import EarningsInformation
from models.previous_earnings_information import PreviousEarningsInformation
from report_building.earnings_builder import EarningsBuilder
from utils.enums.language import Language
from utils.localization import Localization


class TestEarningsBuilder:
    """test class for earnings_builder unit tests."""

    def test__build_markdown_correct_data__markdown_string_returned(
        self, mock_earn_graph_builder, create_earnings_info: list[EarningsInformation]
    ):
        """Test that checks if markdown string is built correctly when correct data is given and graph builder works."""
        loc = Localization(Language.ENGLISH)
        earnings_builder = EarningsBuilder(loc)
        md_string = earnings_builder.build_markdown(create_earnings_info)

        assert loc.translate("earnings_title") in md_string
        assert loc.translate("earnings_intro") in md_string

        for earn in create_earnings_info:
            assert earn.name in md_string

        assert md_string.count(loc.translate("earnings_price_chart")) == 12

    def test__build_markdown_no_data__markdown_string_no_earnings_returned(
        self, mock_earn_graph_builder
    ):
        """Check if build markdown returns md string with only title and intro when no earnings data is given."""
        loc = Localization(Language.ENGLISH)
        earnings_builder = EarningsBuilder(loc)
        md_string = earnings_builder.build_markdown([])

        assert loc.translate("earnings_title") in md_string
        assert loc.translate("earnings_intro") in md_string

        assert loc.translate("earnings_date") not in md_string
        assert loc.translate("earnings_revenue") not in md_string
        assert loc.translate("earnings_price_chart") not in md_string

    def test__build_markdown_graph_builder_fails__markdown_string_no_graphs(
        self,
        mock_false_earn_graph_builder,
        create_earnings_info: list[EarningsInformation],
    ):
        """Check if build markdown returns md string with all other data except for graph when graph buidler isn't working."""
        loc = Localization(Language.ENGLISH)
        earnings_builder = EarningsBuilder(loc)
        md_string = earnings_builder.build_markdown(create_earnings_info)

        assert loc.translate("earnings_title") in md_string
        assert loc.translate("earnings_intro") in md_string

        for earn in create_earnings_info:
            assert earn.name in md_string

        assert loc.translate("earnings_price_chart") not in md_string

    def test__build_markdown_no_eps__markdown_string_with_NA(
        self, mock_earn_graph_builder
    ):
        """Check if build markdown is generated with N/A values for EPS when no EPS is provided"""
        earn_info = EarningsInformation(
            "TCK", "TCK", [], 123, None, datetime.now(), 123, []
        )
        loc = Localization(Language.ENGLISH)
        earnings_builder = EarningsBuilder(loc)
        md_string = earnings_builder.build_markdown([earn_info])

        assert md_string.count("N/A") == 3

    def test__build_markdown_prev_earn__markdown_string_with_prev_earn(
        self, mock_earn_graph_builder
    ):
        """Check if build markdown generates correct string when prev eranings data is provided by Earnings info."""
        earn_info = EarningsInformation(
            "TCK",
            "TCK",
            [],
            123,
            None,
            datetime.now(),
            123,
            [
                PreviousEarningsInformation(1, 2, 3),
                PreviousEarningsInformation(1, 2, 3),
                PreviousEarningsInformation(1, 2, 3),
                PreviousEarningsInformation(1, 2, 3),
            ],
        )
        loc = Localization(Language.ENGLISH)
        earnings_builder = EarningsBuilder(loc)
        md_string = earnings_builder.build_markdown([earn_info])

        assert md_string.count("|") == 30
