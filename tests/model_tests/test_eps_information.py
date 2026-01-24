from models.eps_information import EpsInformation


class TestEpsInformation:
    """Test class for EpsInformation model."""

    def test__create_eps_information__fields_have_given_values(self):
        """Test that EpsInformation is created correctly."""
        eps = EpsInformation(avg=1.5, low=1.2, high=1.8)
        assert eps.avg == 1.5
        assert eps.low == 1.2
        assert eps.high == 1.8

    def test__to_dict_eps_information__dict_returned_with_given_values(self):
        """Test that to_dict returns correct dictionary."""
        eps = EpsInformation(avg=1.0, low=0.8, high=1.2)
        assert eps.to_dict() == {"avg": 1.0, "low": 0.8, "high": 1.2}
