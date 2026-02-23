from models.eps_information import EpsInformation


class TestEpsInformation:
    """Test class for EpsInformation model."""

    def test__create_eps_information__fields_have_given_values(self, create_eps_info: EpsInformation):
        """Test that EpsInformation is created correctly."""
        eps = create_eps_info
        assert eps.avg == 1.5
        assert eps.low == 1.2
        assert eps.high == 1.8

    def test__to_dict_eps_information__dict_returned_with_given_values(self, create_eps_info: EpsInformation):
        """Test that to_dict returns correct dictionary."""
        eps = create_eps_info
        assert eps.to_dict() == {"avg": 1.5, "low": 1.2, "high": 1.8}
