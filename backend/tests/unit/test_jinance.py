import pytest

from jinance import Jinance


class TestJinance:
    """Test class for Jinance tests."""

    @pytest.mark.skip(reason="Implementation changed, will fix soon.")
    def test__generate_report__path_to_report(
        self,
    ):
        """Check if initializing Jinance works, and if generate_report method returns a string representation of a path to where the report is generated."""
        jinance = Jinance()

        assert jinance.generate_report(5) == "path/to/report"
