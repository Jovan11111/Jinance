class AggregatedInsiderInfo:
    def __init__(self, ticker: str, bought: float, sold: float):
        self._ticker = ticker
        self._bought = bought if bought >= 0 else 0
        self._sold = sold if sold >= 0 else 0

    @property
    def ticker(self) -> str:
        """Getter for the ticker of the filtered insider trading information."""
        return self._ticker

    @property
    def bought(self) -> float:
        """Getter for the total value of bought insider trading information."""
        return self._bought

    @property
    def sold(self) -> float:
        """Getter for the total value of sold insider trading information."""
        return self._sold

    def to_dict(self) -> dict:
        """Convert FilteredInsiderInfo object to a dictionary."""
        return {
            "ticker": self.ticker,
            "bought": self.bought,
            "sold": self.sold,
        }
