import yfinance as yf

from models.price_performance_information import PricePerformanceInformation
from providers.price_performance_provider import PricePerformanceProvider


class YahooPricePerformanceProvider(PricePerformanceProvider):

    def fetch_price_performance(
        self, tickers: list[str], days_behind: int
    ) -> list[PricePerformanceInformation]:
        """Get prices for all tickers in a given time period with yahoo API.

        Args:
            tickers (list[str]): List of tickers for which to get prices.
            days_behind (int): How many days behind to get prices for.

        Returns:
            list[PricePerformanceInformation]: List of price performances for all tickers.
        """
        result: list[PricePerformanceInformation] = []
        for ticker in tickers:
            try:
                stock = yf.Ticker(ticker)
                hist = stock.history(period=f"{days_behind}d")
                if not hist.empty:
                    result.append(
                        PricePerformanceInformation(
                            ticker, hist["Close"].round(2).tolist()
                        )
                    )
            except Exception as e:
                print(f"Error fetching price performance for {ticker}: {e}")
                continue
        return result
