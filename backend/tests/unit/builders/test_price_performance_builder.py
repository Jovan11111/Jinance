from models.price_performance_information import PricePerformanceInformation
from report_building.price_performance_builder import PricePerformanceBuilder
from utils.enums.language import Language
from utils.localization import Localization


class TestPricePerformanceBuilder:
    """Test class for Price performance builder tests."""

    def test__build_markdown_correct_data__md_string_returned(
        self,
        mock_pp_graph_builder,
        create_price_perf_dict: dict[str, list[PricePerformanceInformation]],
    ):
        """Check if build markdown returns a correct md string when data is given."""
        loc = Localization(Language.ENGLISH)
        price_performance_builder = PricePerformanceBuilder(loc)
        md_string = price_performance_builder.build_markdown(create_price_perf_dict)

        assert loc.translate("price_perf_title") in md_string
        assert loc.translate("price_perf_intro") in md_string

        for price_perf in create_price_perf_dict["winners"]:
            assert price_perf.ticker in md_string

        for price_perf in create_price_perf_dict["losers"]:
            assert price_perf.ticker in md_string

    def test__build_markdown_no_data__md_string_no_price_perf(
        self, mock_pp_graph_builder
    ):
        """Check if build markdown returns a md string with no price performance when no price performance is given."""
        loc = Localization(Language.ENGLISH)
        price_performance_builder = PricePerformanceBuilder(loc)
        md_string = price_performance_builder.build_markdown(
            {"winners": [], "losers": []}
        )

        assert loc.translate("price_perf_title") in md_string
        assert loc.translate("price_perf_intro") in md_string
        assert loc.translate("price_perf_best") not in md_string
        assert loc.translate("price_perf_worst") not in md_string
