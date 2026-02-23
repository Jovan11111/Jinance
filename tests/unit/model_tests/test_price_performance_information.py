from models.price_performance_information import PricePerformanceInformation


class TestPricePerformanceInformation:
    """Test class for PricePerformanceInformation model."""

    def test__create_price_performance_information__fields_have_given_values(self, create_price_perf: PricePerformanceInformation):
        """Test that PricePerformanceInformation is created correctly."""
        price_info = create_price_perf
        assert price_info.ticker == "TCK1"
        assert price_info.prices == [10.0, 20.12, 12.64, 14.32, 15.01, 7.62, 8.0]
        assert price_info.percent_change == -20.0

    def test__create_price_performance_information_with_insufficient_prices__percent_change_is_zero(
        self,
    ):
        """Test that percent_change is 0.0 when there are insufficient prices."""
        price_info = PricePerformanceInformation(
            ticker="some_ticker",
            prices=[10.0],
        )
        assert price_info.percent_change == 0.0

    def test__to_dict_price_performance_information__dict_returned_with_given_values(
        self, create_price_perf: PricePerformanceInformation
    ):
        """Test that to_dict returns correct dictionary."""

        price_info = create_price_perf
        assert price_info.to_dict() == {
            "ticker": "TCK1",
            "prices": [10.0, 20.12, 12.64, 14.32, 15.01, 7.62, 8.0],
            "percent_change": -20.0,
        }
