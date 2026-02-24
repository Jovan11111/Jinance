
from unittest.mock import MagicMock

import pytest

from jinance import Jinance




class TestJinance:
    """Test class for Jinance tests."""

    def test__generate_report__path_to_report(self, mock_earnings_manager, mock_news_manager, mock_price_performance_manager, mock_report_builder):
        """Check if initializing Jinance works, and if generate_report method returns a string representation of a path to where the report is generated."""
        jinance = Jinance()

        assert jinance.generate_report(5) == "path/to/report"
