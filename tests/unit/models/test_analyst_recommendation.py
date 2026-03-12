from models.analyst_recommendation import AnalystRecommendation


class TestAnalystRecommendation:
    """Test class for AnalystRecommendation model."""

    def test__create_analyst_recommendation__fields_have_given_values(
        self, create_analyst_recommendation: AnalystRecommendation
    ):
        """Test that AnalystRecommendation is created correctly."""
        rec = create_analyst_recommendation
        assert rec.ticker == "TCK"
        assert rec.index == 56

    def test__to_dict_analyst_recommendation__dict_returned_with_given_values(
        self, create_analyst_recommendation: AnalystRecommendation
    ):
        """Test that to_dict returns correct dictionary."""
        rec = create_analyst_recommendation
        assert rec.to_dict() == {"ticker": "TCK", "index": 56}

    def test__create_false_analyst_recommendation__index_set_to_0(
        self, create_false_analyst_recommendation: AnalystRecommendation
    ):
        """Test that AnalystRecommendation is created correctly with false index."""
        rec = create_false_analyst_recommendation
        assert rec.ticker == "TCK"
        assert rec.index == 0
