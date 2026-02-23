from models.previous_earnings_information import PreviousEarningsInformation


class TestPreviousEarningsInformation:
    """Test class for PreviousEarningsInformation model."""

    def test__create_previous_earnings_information__fields_have_given_values(self, create_prev_eps_info: PreviousEarningsInformation):
        """Test that PreviousEarningsInformation is created correctly."""
        pei = create_prev_eps_info
        assert pei.expected_eps == 1.5
        assert pei.actual_eps == 1.4
        assert pei.price_diff == 0.1

    def test__to_dict_previous_earnings_information__dict_returned_with_given_values(
        self, create_prev_eps_info: PreviousEarningsInformation
    ):
        """Test that to_dict returns correct dictionary."""
        pei = create_prev_eps_info
        assert pei.to_dict() == {
            "expected_eps": 1.5,
            "actual_eps": 1.4,
            "price_diff": 0.1,
        }
