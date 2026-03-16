from managers.earnings_manager import EarningsManager


class TestEarningsManager:
    """Test class for Earnings manager tests."""

    def test__get_earnings_provided_regular_info__correct_number_of_information_returned(
        self, mock_yahoo_earnings_provider
    ):
        """Check if get_latest_upcoming_earnings returns correct number of information when provider returns regular information."""
        earnings_manager = EarningsManager()
        result = earnings_manager.get_latest_upcoming_earnings(5)

        assert len(result) == 5
        expected_tickers = [
            e.ticker
            for e in sorted(
                mock_yahoo_earnings_provider.fetch_earnings.return_value,
                key=lambda x: x.date,
            )[:5]
        ]
        assert [r.ticker for r in result] == expected_tickers

    def test__get_earnings_provided_no_information__empty_list_returned(
        self, mock_yahoo_earnings_provider
    ):
        """Check if get_latest_upcoming_earnings returns empty list when provider returns empty list."""
        mock_yahoo_earnings_provider.fetch_earnings.return_value = []
        earnings_manager = EarningsManager()
        result = earnings_manager.get_latest_upcoming_earnings(5)

        assert result == []

    def test__get_earnings_provided_less_information_than_requested__all_information_returned(
        self, mock_yahoo_earnings_provider
    ):
        """Check if get_latest_upcoming_earnings returns all information when provider returns less information than requested."""
        mock_yahoo_earnings_provider.fetch_earnings.return_value = (
            mock_yahoo_earnings_provider.fetch_earnings.return_value[:3]
        )
        earnings_manager = EarningsManager()
        result = earnings_manager.get_latest_upcoming_earnings(5)

        assert len(result) == 3
        expected_tickers = [
            e.ticker
            for e in sorted(
                mock_yahoo_earnings_provider.fetch_earnings.return_value,
                key=lambda x: x.date,
            )
        ]
        assert [r.ticker for r in result] == expected_tickers

    def test__get_earnings_provided_list_of_null_values__returns_empty_list(
        self, mock_yahoo_earnings_provider
    ):
        """Check if get_latest_upcoming_earnings returns empty list when provider returns list of null values."""
        mock_yahoo_earnings_provider.fetch_earnings.return_value = [None] * 15
        earnings_manager = EarningsManager()
        result = earnings_manager.get_latest_upcoming_earnings(5)

        assert result == []

    def test__get_earnings_non_existent_provider__earnings_with_yahoo_provider(
        self, mock_yahoo_earnings_provider
    ):
        """Check if providing a manager with non existent provider defaults provider to yahoo."""
        earnings_manager = EarningsManager(provider="NON_EXISTENT")
        result = earnings_manager.get_latest_upcoming_earnings(5)

        assert len(result) == 5
        expected_tickers = [
            e.ticker
            for e in sorted(
                mock_yahoo_earnings_provider.fetch_earnings.return_value,
                key=lambda x: x.date,
            )[:5]
        ]
        assert [r.ticker for r in result] == expected_tickers
