from models.earnings_information import EarningsInformation
from models.eps_information import EpsInformation


class TestEarningsInformation:
    """Test class for EarningsInformation model."""

    def test__create_earnings_information__fields_have_given_values(
        self, create_eps_info: EpsInformation, create_earn_info: EarningsInformation
    ):
        """Test that EarningsInformation is created correctly."""
        epsi = create_eps_info
        ei = create_earn_info
        assert ei.ticker == "TCK"
        assert ei.name == "company"
        assert ei.value_last_15_days == [1.2, 2.3, 3.4]
        assert ei.market_cap == 123456
        assert ei.eps == epsi
        assert ei.date is None
        assert ei.revenue == 1234567
        assert ei.previous_earnings == []

    def test__to_dictearnings_information__dict_returned_with_given_values(
        self, create_eps_info: EpsInformation, create_earn_info: EarningsInformation
    ):
        """Test that to_dict returns correct dictionary."""
        ei = create_earn_info

        assert ei.to_dict() == {
            "ticker": "TCK",
            "name": "company",
            "value_last_15_days": [1.2, 2.3, 3.4],
            "market_cap": 123456,
            "eps": {"avg": 1.5, "low": 1.2, "high": 1.8},
            "date": "",
            "revenue": 1234567,
            "previous_earnings": [],
        }
