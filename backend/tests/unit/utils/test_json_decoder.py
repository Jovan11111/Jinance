from pathlib import Path

from utils.json_decoder import JsonDecoder


class TestJsonDecoder:
    """Test class for JsonDecoder tests."""

    def test__decode_test_config_file__correct_section_data_returned(self):
        """Check if decode function decodes the config file correctly."""
        config_file = Path(__file__).parent.joinpath("test_config_file.json")
        result = JsonDecoder.decode(config_file)

        assert len(result) == 5

        assert result[0].to_dict() == {
            "type": "earnings",
            "language": "en",
            "provider": "yahoo",
            "tickers": ["TCK"],
            "days_ahead": 30,
            "days_behind": None,
            "number_of_companies": 5,
        }
        assert result[1].to_dict() == {
            "type": "news",
            "language": "en",
            "provider": "yahoo",
            "tickers": ["TCK"],
            "days_ahead": None,
            "days_behind": 1,
            "number_of_companies": 10,
        }
        assert result[2].to_dict() == {
            "type": "price_performance",
            "language": "en",
            "provider": "yahoo",
            "tickers": ["TCK"],
            "days_ahead": None,
            "days_behind": 180,
            "number_of_companies": 3,
        }
        assert result[3].to_dict() == {
            "type": "insider_trades",
            "language": "en",
            "provider": "yahoo",
            "tickers": [
                "AAPL",
                "MSFT",
                "GOOGL",
                "GOOG",
                "AMZN",
                "NVDA",
                "META",
                "TSLA",
                "BRK-B",
                "UNH",
            ],
            "days_ahead": None,
            "days_behind": 30,
            "number_of_companies": 3,
        }
        assert result[4].to_dict() == {
            "type": "analyst_ratings",
            "language": "en",
            "provider": "yahoo",
            "tickers": [
                "AAPL",
                "MSFT",
                "GOOGL",
                "GOOG",
                "AMZN",
                "NVDA",
                "META",
                "TSLA",
                "BRK-B",
                "UNH",
            ],
            "days_ahead": None,
            "days_behind": None,
            "number_of_companies": 3,
        }
