from datetime import datetime, timedelta
from unittest.mock import MagicMock

import pytest

from managers.earnings_manager import EarningsManager
from models.earnings_information import EarningsInformation
from models.eps_information import EpsInformation
from providers.yahoo.yahoo_earnings_provider import YahooEarningsProvider
from utils import constants


class TestEarningsManager:
    """Test class for Earnigns manager tests."""

    def test__initialize_earnings_manager__all_fields_correct(self):
        """Check if initializiting manager with reasonable values creates Earnings manager correctly."""
        earnings_manager = EarningsManager("yahoo", 25, constants.TICKERS_SP_20)

        assert earnings_manager.days_ahead == 25
        assert earnings_manager.tickers == constants.TICKERS_SP_20
        assert isinstance(earnings_manager.provider, YahooEarningsProvider)

    def test__initalize_earnings_manager_negative_days_ahead__initialized_with_default_days_ahead_value(
        self,
    ):
        """Check if Earnings manager will be initialized with default values for days_ahead if given value makes no sense."""
        earnings_manager = EarningsManager("yahoo", -5214, constants.TICKERS_SP_20)

        assert earnings_manager.days_ahead == 30
        assert earnings_manager.tickers == constants.TICKERS_SP_20
        assert isinstance(earnings_manager.provider, YahooEarningsProvider)

    def test__initialize_earnings_manager_default_values__initializes_with_default_values(
        self,
    ):
        """Check if Earnigns Manager will be initialized with default values if no other are given."""
        earnings_manager = EarningsManager()

        assert earnings_manager.days_ahead == 30
        assert earnings_manager.tickers == constants.TICKERS_SP_100
        assert isinstance(earnings_manager.provider, YahooEarningsProvider)

    def test__initialize_earnings_manager_non_existant_provider__initizes_with_default_value(
        self,
    ):
        """Check if Earnings Manager will be initialized with default values if non existant provider name is given."""
        earnings_manager = EarningsManager("NON_EXISTANT", 30, constants.TICKERS_SP_10)

        assert earnings_manager.days_ahead == 30
        assert earnings_manager.tickers == constants.TICKERS_SP_10
        assert isinstance(earnings_manager.provider, YahooEarningsProvider)

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
