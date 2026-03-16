from jinance import Jinance


class TestJinance:
    """Test class for Jinance tests."""

    def test__generate_report__path_to_report(
        self, mock_report_builder_director, mock_json_decoder
    ):
        """Check if initializing Jinance works, and if generate_report method returns a string representation of a path to where the report is generated."""
        jinance = Jinance()

        assert jinance.generate_report() == "path/to/report"
