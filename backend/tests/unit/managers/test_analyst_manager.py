from managers.analyst_manager import AnalystManager


class TestAnalystManager:
    """Test class for Analyst manager tests."""

    def test__get_analyst_recommendations__returns_dict_with_recommendations(
        self, mock_yahoo_analyst_provider, create_analyst_recommendations
    ):
        """Check if returns a dict with buy and sell recommendations."""

        analyst_manager = AnalystManager()
        result = analyst_manager.get_analyst_recommendations(3)
        assert result == {
            "buy": create_analyst_recommendations[::-1][:3],
            "sell": create_analyst_recommendations[:3][::-1],
        }

    def test__get_analyst_recommendations_negative_companies__3_companies(
        self, mock_yahoo_analyst_provider, create_analyst_recommendations
    ):
        """Check if number of companies is defaulted to 3 when negative argument is received."""

        analyst_manager = AnalystManager()
        result = analyst_manager.get_analyst_recommendations(-1)
        assert result == {
            "buy": create_analyst_recommendations[::-1][:3],
            "sell": create_analyst_recommendations[:3][::-1],
        }

    def test__get_analyst_recommendations_non_existent_provider__yahoo_provider_chosen(
        self, mock_yahoo_analyst_provider, create_analyst_recommendations
    ):
        analyst_manager = AnalystManager(provider="NON_EXISTENT")
        result = analyst_manager.get_analyst_recommendations(3)
        assert result == {
            "buy": create_analyst_recommendations[::-1][:3],
            "sell": create_analyst_recommendations[:3][::-1],
        }
