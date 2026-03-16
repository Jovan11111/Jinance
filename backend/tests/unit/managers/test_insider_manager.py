from managers.insider_manager import InsiderManager


class TestInsiderManager:
    """Test class for Insider manager tests."""

    def test__get_insider_trades__returns_aggregated_insider_info(
        self, mock_yahoo_insider_provider, mock_insider_filter, create_insider_trades
    ):
        """Check if calling get_insider_trades regularly returns correct values."""
        insider_manager = InsiderManager()
        result = insider_manager.get_insider_trades(3)
        assert len(result["buyers"]) == 3
        assert len(result["sellers"]) == 3
        assert result["buyers"][0].ticker == "TCK1"
        assert result["buyers"][0].bought == 3000.0
        assert result["buyers"][0].sold == 0.0
        assert result["buyers"][1].ticker == "TCK3"
        assert result["buyers"][1].bought == 2000.0
        assert result["buyers"][1].sold == 0.0
        assert result["buyers"][2].ticker == "TCK5"
        assert result["buyers"][2].bought == 1000.0
        assert result["buyers"][2].sold == 0.0
        assert result["sellers"][0].ticker == "TCK2"
        assert result["sellers"][0].bought == 0.0
        assert result["sellers"][0].sold == 6000.0
        assert result["sellers"][1].ticker == "TCK4"
        assert result["sellers"][1].bought == 0.0
        assert result["sellers"][1].sold == 3000.0
        assert result["sellers"][2].ticker == "TCK6"
        assert result["sellers"][2].bought == 0.0
        assert result["sellers"][2].sold == 1000.0

    def test__get_insider_trades_negative_companies__returns_aggregated_insider_info(
        self, mock_yahoo_insider_provider, mock_insider_filter, create_insider_trades
    ):
        """Check if calling get_insider_trades with negative number_of_companies arguments defaults the arguments to 3."""
        insider_manager = InsiderManager()
        result = insider_manager.get_insider_trades(-1)
        assert len(result["buyers"]) == 3
        assert len(result["sellers"]) == 3
        assert result["buyers"][0].ticker == "TCK1"
        assert result["buyers"][0].bought == 3000.0
        assert result["buyers"][0].sold == 0.0
        assert result["buyers"][1].ticker == "TCK3"
        assert result["buyers"][1].bought == 2000.0
        assert result["buyers"][1].sold == 0.0
        assert result["buyers"][2].ticker == "TCK5"
        assert result["buyers"][2].bought == 1000.0
        assert result["buyers"][2].sold == 0.0
        assert result["sellers"][0].ticker == "TCK2"
        assert result["sellers"][0].bought == 0.0
        assert result["sellers"][0].sold == 6000.0
        assert result["sellers"][1].ticker == "TCK4"
        assert result["sellers"][1].bought == 0.0
        assert result["sellers"][1].sold == 3000.0
        assert result["sellers"][2].ticker == "TCK6"
        assert result["sellers"][2].bought == 0.0
        assert result["sellers"][2].sold == 1000.0

    def test__get_insider_trades_non_existent_provider__returns_aggregated_insider_info(
        self, mock_yahoo_insider_provider, mock_insider_filter, create_insider_trades
    ):
        """Check if calling get_insider_trades with non existent provider default it to yahoo."""
        insider_manager = InsiderManager(provider="NON_EXISTENT")
        result = insider_manager.get_insider_trades(3)
        assert len(result["buyers"]) == 3
        assert len(result["sellers"]) == 3
        assert result["buyers"][0].ticker == "TCK1"
        assert result["buyers"][0].bought == 3000.0
        assert result["buyers"][0].sold == 0.0
        assert result["buyers"][1].ticker == "TCK3"
        assert result["buyers"][1].bought == 2000.0
        assert result["buyers"][1].sold == 0.0
        assert result["buyers"][2].ticker == "TCK5"
        assert result["buyers"][2].bought == 1000.0
        assert result["buyers"][2].sold == 0.0
        assert result["sellers"][0].ticker == "TCK2"
        assert result["sellers"][0].bought == 0.0
        assert result["sellers"][0].sold == 6000.0
        assert result["sellers"][1].ticker == "TCK4"
        assert result["sellers"][1].bought == 0.0
        assert result["sellers"][1].sold == 3000.0
        assert result["sellers"][2].ticker == "TCK6"
        assert result["sellers"][2].bought == 0.0
        assert result["sellers"][2].sold == 1000.0
