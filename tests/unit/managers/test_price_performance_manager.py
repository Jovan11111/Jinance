from managers.price_performance_manager import PricePerformanceManager
from providers.yahoo.yahoo_price_performance_provider import (
    YahooPricePerformanceProvider,
)
from utils import constants


class TestPricePerformanceManager:
    """Test class for Price performance manager tests."""

    def test__initialize_pp_manager_regular_data__fields_filled_regularly(self):
        """Check if initializing price performance manager with default data initializes it correctly."""
        pp_manager = PricePerformanceManager("yahoo", 123, constants.TICKERS_SP_50)

        assert pp_manager.days_ahead == 123
        assert pp_manager.tickers == constants.TICKERS_SP_50
        assert isinstance(pp_manager.provider, YahooPricePerformanceProvider)

    def test__initialize_pp_manager_negative_days_ahead__fields_initialize_with_default_value(
        self,
    ):
        """Check if initializing price performance manager with negative days ahead initializes it with default days ahead."""
        pp_manager = PricePerformanceManager("yahoo", -15, constants.TICKERS_SP_50)

        assert pp_manager.days_ahead == 180
        assert pp_manager.tickers == constants.TICKERS_SP_50
        assert isinstance(pp_manager.provider, YahooPricePerformanceProvider)

    def test__initialize_pp_manager_with_default_values__initialized_with_default_values(
        self,
    ):
        """Check if PP manager is initialized with default values when no other are given."""
        pp_manager = PricePerformanceManager()

        assert pp_manager.days_ahead == 180
        assert pp_manager.tickers == constants.TICKERS_SP_100
        assert isinstance(pp_manager.provider, YahooPricePerformanceProvider)

    def test__initialize_pp_manager_non_existant_provider__initialized_with_default_provider(
        self,
    ):
        """Check if PP manager is initialized with default provider, if a fake provider is given."""
        pp_manager = PricePerformanceManager(
            "NON_EXISTANT", 456, constants.TICKERS_SP_10
        )

        assert pp_manager.days_ahead == 456
        assert pp_manager.tickers == constants.TICKERS_SP_10
        assert isinstance(pp_manager.provider, YahooPricePerformanceProvider)

    def test__get_price_performance_good_data__return_list_of_winners_and_losers(
        self, mock_yahoo_price_performance_provider
    ):
        """Check if get_worst_best_price_performance returns correct values when given good data."""
        pp_manager = PricePerformanceManager()
        result = pp_manager.get_best_worst_price_performance(3)
        assert len(result["winners"]) == 3
        assert len(result["losers"]) == 3
        assert result["winners"][0].ticker == "TCK3"
        assert result["winners"][1].ticker == "TCK11"
        assert result["winners"][2].ticker == "TCK13"

        assert result["losers"][0].ticker == "TCK9"
        assert result["losers"][1].ticker == "TCK10"
        assert result["losers"][2].ticker == "TCK7"

    def test__get_price_performance_empty_list__returns_empty_list(
        self, mock_yahoo_price_performance_provider
    ):
        """Check if get_worst_best_price_performance returns an empty list if no data is provided to it."""
        mock_yahoo_price_performance_provider.fetch_price_performance.return_value = []
        pp_manager = PricePerformanceManager()
        result = pp_manager.get_best_worst_price_performance(3)
        assert result == {"winners": [], "losers": []}

    def test__get_price_performance_negative_number_of_companies__sets_number_of_companies_to_3(
        self, mock_yahoo_price_performance_provider
    ):
        """Check if get_worst_best_price_performance works correclly even with bad user input."""
        pp_manager = PricePerformanceManager()
        result = pp_manager.get_best_worst_price_performance(-4)
        assert len(result["winners"]) == 3
        assert len(result["losers"]) == 3

    def test__get_price_performance_small_data__returns_lesser_winners_losers(
        self, mock_yahoo_price_performance_provider, create_price_performance_info
    ):
        """Check if get_worst_best_price_performance returns same for winners and losers when there are less tickers then companies."""
        mock_yahoo_price_performance_provider.fetch_price_performance.return_value = (
            create_price_performance_info[:2]
        )
        pp_manager = PricePerformanceManager()
        result = pp_manager.get_best_worst_price_performance(3)
        assert len(result["winners"]) == 2
        assert len(result["losers"]) == 2

        assert result["winners"][0].ticker == "TCK2"
        assert result["winners"][1].ticker == "TCK1"

        assert result["losers"][0].ticker == "TCK2"
        assert result["losers"][1].ticker == "TCK1"
