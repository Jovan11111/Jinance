class PricePerformanceInformation:
    """Class that represents price performance information for a given ticker."""

    def __init__(self, ticker: str, prices: list[float]):
        self._ticker = ticker
        self._prices = prices

    @property
    def ticker(self) -> str:
        """Getter for the ticker symbol."""
        return self._ticker

    @property
    def prices(self) -> list[float]:
        """Getter for the list of prices."""
        return self._prices

    @property
    def percent_change(self) -> float:
        """Calculate the percent change from the first to the last price, so the difference from beggining to end."""
        if not self._prices or len(self._prices) < 2:
            return 0.0
        return round(((self._prices[-1] - self._prices[0]) / self._prices[0]) * 100, 2)

    def to_dict(self) -> dict:
        """Convert PricePerformanceInformation object to a dictionary."""
        return {
            "ticker": self._ticker,
            "prices": self._prices,
            "percent_change": self.percent_change,
        }
