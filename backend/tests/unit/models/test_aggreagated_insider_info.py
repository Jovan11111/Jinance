from models.aggregated_insider_info import AggregatedInsiderInfo


class TestAggregatedInsiderInfo:
    """Test class for AggregatedInsiderInfo model."""

    def test__create_aggregated_insider_info__fields_have_given_values(
        self, create_aggregated_insider_information: AggregatedInsiderInfo
    ):
        """Test that AggregatedInsiderInfo is created correctly."""
        agg_ins_info = create_aggregated_insider_information
        assert agg_ins_info.ticker == "TCK"
        assert agg_ins_info.bought == 100
        assert agg_ins_info.sold == 200

    def test__to_dict_aggregated_insider_info__dict_returned_with_given_values(
        self, create_aggregated_insider_information: AggregatedInsiderInfo
    ):
        """Test that to_dict returns correct dictionary."""
        agg_ins_info = create_aggregated_insider_information
        assert agg_ins_info.to_dict() == {"ticker": "TCK", "bought": 100, "sold": 200}

    def test__create_false_aggregated_insider_info__fields_have_default_values(
        self, create_false_aggregated_insider_information: AggregatedInsiderInfo
    ):
        """Test that AggregatedInsiderInfo is created with default values when given negative values."""
        agg_ins_info = create_false_aggregated_insider_information
        assert agg_ins_info.ticker == "TCK"
        assert agg_ins_info.bought == 0
        assert agg_ins_info.sold == 0
