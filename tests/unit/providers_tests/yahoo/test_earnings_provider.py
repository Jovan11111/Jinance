import pytest


@pytest.fixture
def mock_yf_ticker(mocker):
    return mocker.patch("providers.yahoo.yahoo_news_provider.yf.Ticker")


class TestEearningsProvider:
    def test__fetch_earnings_multiple_tickers__return_earnings_list(self):
        pass

    def test__fetch_earnings_no_content__skips_earning(self):
        pass

    def test__fetch_earnings_no_content__returns_empty_list(self):
        pass

    def test__fetch_earnings_empty_fields__returns_empty_earnings_object(self):
        pass
