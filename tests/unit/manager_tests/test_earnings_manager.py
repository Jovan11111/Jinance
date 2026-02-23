from datetime import datetime
from unittest.mock import MagicMock
from managers.earnings_manager import EarningsManager
from models.earnings_information import EarningsInformation
from models.eps_information import EpsInformation
from providers.yahoo.yahoo_earnings_provider import YahooEarningsProvider
from providers.yahoo.yahoo_earnings_provider import YahooEarningsProvider
from utils import constants
import pytest

@pytest.fixture()
def create_earnings_info() -> list[EarningsInformation]:
    return [
        EarningsInformation("TCK1", "company1", [], 123456, EpsInformation(1, 2, 3), datetime(2026, 4, 9, 12, 0, 0), 321, []),
        EarningsInformation("TCK2", "company2", [], 123456, EpsInformation(1, 2, 3), datetime(2026, 4, 9, 12, 0, 0), 321, []),
        EarningsInformation("TCK3", "company3", [], 123456, EpsInformation(1, 2, 3), datetime(2026, 4, 9, 12, 0, 0), 321, []),
        EarningsInformation("TCK4", "company4", [], 123456, EpsInformation(1, 2, 3), datetime(2026, 4, 9, 12, 0, 0), 321, []),
        EarningsInformation("TCK5", "company5", [], 123456, EpsInformation(1, 2, 3), datetime(2026, 4, 9, 12, 0, 0), 321, []),
        EarningsInformation("TCK6", "company6", [], 123456, EpsInformation(1, 2, 3), datetime(2026, 4, 9, 12, 0, 0), 321, []),
        EarningsInformation("TCK7", "company7", [], 123456, EpsInformation(1, 2, 3), datetime(2026, 4, 9, 12, 0, 0), 321, []),
        EarningsInformation("TCK8", "company8", [], 123456, EpsInformation(1, 2, 3), datetime(2026, 4, 9, 12, 0, 0), 321, []),
        EarningsInformation("TCK9", "company9", [], 123456, EpsInformation(1, 2, 3), datetime(2026, 4, 9, 12, 0, 0), 321, []),
        EarningsInformation("TCK10", "company10", [], 123456, EpsInformation(1, 2, 3), datetime(2026, 4, 9, 12, 0, 0), 321, []),
        EarningsInformation("TCK11", "company11", [], 123456, EpsInformation(1, 2, 3), datetime(2026, 4, 9, 12, 0, 0), 321, []),
        EarningsInformation("TCK12", "company12", [], 123456, EpsInformation(1, 2, 3), datetime(2026, 4, 9, 12, 0, 0), 321, []),
    ]

@pytest.fixture
def mock_yahoo_provider(mocker, create_earnings_info):
    mock_cls = mocker.patch("managers.earnings_manager.YahooEarningsProvider")
    mock_instance = mock_cls.return_value
    mock_instance.fetch_earnings.return_value = create_earnings_info
    return mock_instance

class TestEarningsManager:
    """Test class for Earnigns manager tests."""

    def test__initialize_earnings_manager__all_fields_correct(self):
        """Check if initializiting manager with reasonable values creates Earnings manager correctly."""
        earnings_manager = EarningsManager("yahoo", 25, constants.TICKERS_SP_20)

        assert earnings_manager.days_ahead == 25
        assert earnings_manager.tickers == constants.TICKERS_SP_20
        assert isinstance(earnings_manager.provider, YahooEarningsProvider)

    def test__initalize_earnings_manager_negative_days_ahead__initialized_with_default_days_ahead_value(self):
        """Check if Earnings manager will be initialized with default values for days_ahead if given value makes no sense."""
        earnings_manager = EarningsManager("yahoo", -5214, constants.TICKERS_SP_20)

        assert earnings_manager.days_ahead == 30
        assert earnings_manager.tickers == constants.TICKERS_SP_20
        assert isinstance(earnings_manager.provider, YahooEarningsProvider)

    def test__initialize_earnings_manager_default_values__initializes_with_default_values(self):
        """Check if Earnigns Manager will be initialized with default values if no other are given."""
        earnings_manager = EarningsManager()

        assert earnings_manager.days_ahead == 30
        assert earnings_manager.tickers == constants.TICKERS_SP_100
        assert isinstance(earnings_manager.provider, YahooEarningsProvider)

    def test__initialize_earnings_manager_non_existant_provider__initizes_with_default_value(self):
        """Check if Earnings Manager will be initialized with default values if non existant provider name is given."""
        earnings_manager = EarningsManager("NON_EXISTANT", 30, constants.TICKERS_SP_10)

        assert earnings_manager.days_ahead == 30
        assert earnings_manager.tickers == constants.TICKERS_SP_10
        assert isinstance(earnings_manager.provider, YahooEarningsProvider)

    def test__get_earnings_provided_regular_info__correct_number_of_information_returned(mock_yahoo_provider):
        earnings_manager = EarningsManager("yahoo", 150, constants.TICKERS_SP_10)
        import managers.earnings_manager as em
        print(em.YahooEarningsProvider)


        