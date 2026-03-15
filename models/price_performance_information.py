class PricePerformanceInformation:
    """Class that represents price performance information for a given ticker.

    Fields:
        ticker (str): Ticker of the company the price performance is about.
        price (list[float]): List of prices in the last {number_of_days} days.
    """

    def __init__(self, ticker: str, prices: list[float]):
        self.__ticker = ticker
        self.__prices = prices

    @property
    def ticker(self) -> str:
        """Getter for the ticker symbol."""
        return self.__ticker

    @property
    def prices(self) -> list[float]:
        """Getter for the list of prices."""
        return self.__prices

    @property
    def percent_change(self) -> float:
        """Calculate the percent change from the first to the last price, so the difference from beginning to end."""
        if not self.__prices or len(self.__prices) < 2:
            return 0.0
        return round(
            ((self.__prices[-1] - self.__prices[0]) / self.__prices[0]) * 100, 2
        )

    def to_dict(self) -> dict:
        """Convert PricePerformanceInformation object to a dictionary."""
        return {
            "ticker": self.__ticker,
            "prices": self.__prices,
            "percent_change": self.percent_change,
        }
