import utils.constants as constants


class TestConstants:
    """Test class for constants module."""

    def test__all_constants_exist(self):
        """Test that all required constants exist in the constants module."""
        required_constants = [
            "TICKERS_SP_100",
            "TICKERS_SP_50",
            "TICKERS_SP_20",
            "TICKERS_SP_10",
            "TICKER_TO_COMPANY",
            "HARD_EVENT_KEYWORDS",
            "FINANCIAL_KEYWORDS",
            "PRODUCT_KEYWORDS",
            "MANAGEMENT_KEYWORDS",
            "IMPORTANT_KEYWORDS",
        ]

        for const_name in required_constants:
            assert hasattr(constants, const_name)
