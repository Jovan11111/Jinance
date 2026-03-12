from datetime import datetime

from models.insider_information import InsiderInformation
from utils.enums.trade_type import TradeType


class TestInsiderInformation:
    """Test class for InsiderInformation model."""

    def test__create_insider_information__fields_have_given_values(
        self, create_insider_information: InsiderInformation
    ):
        """Test that InsiderInformation is craeted correctly"""
        ins_info = create_insider_information
        assert ins_info.ticker == "TCK"
        assert ins_info.value == 123
        assert ins_info.type == TradeType.BUY
        assert ins_info.date == datetime(2026, 4, 9, 12, 0, 0)

    def test__to_dict_insider_information__dict_returned_with_given_values(
        self, create_insider_information: InsiderInformation
    ):
        """Test that to_dict return correct dictionary."""
        ins_info = create_insider_information
        assert ins_info.to_dict() == {
            "ticker": "TCK",
            "value": 123,
            "type": TradeType.BUY,
            "date": datetime(2026, 4, 9, 12, 0, 0).isoformat(),
        }

    def test__create_false_insider_information__negative_value_set_to_zero(
        self, create_false_insider_information: InsiderInformation
    ):
        """Test that InsiderInformation is created correctly when negative value is given."""
        ins_info = create_false_insider_information
        assert ins_info.ticker == "TCK"
        assert ins_info.value == 0
        assert ins_info.type == TradeType.BUY
        assert ins_info.date == datetime(2026, 4, 9)
