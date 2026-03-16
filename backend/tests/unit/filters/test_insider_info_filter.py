from filters.insider_info_filter import InsiderInfoFilter


class TestInsiderInfoFilter:
    """Test class for InsiderInfoFilter."""

    def test__filter_insider_info_integration__return_3_that_meet_the_criteria(
        self, sample_insider_trades
    ):
        """Test that checks if all filtering functions work together to remove all unnecessary insider info."""
        insider_info_filter = InsiderInfoFilter(7)
        result = insider_info_filter.filter_insider_info(sample_insider_trades)
        assert len(result) == 3
        assert result == sample_insider_trades[:3]
