class AnalystRecommendation:
    def __init__(self, ticker: str, index: float):
        self._ticker = ticker
        self._index = index if index >= -100 and index <= 100 else 0

    @property
    def ticker(self) -> str:
        """Getter for the ticker of the analyst recommendation information."""
        return self._ticker

    @property
    def index(self) -> float:
        """Getter for the index of the analyst recommendation information."""
        return self._index

    def to_dict(self) -> dict:
        """Convert AnalystRecommendation object to a dictionary."""
        return {
            "ticker": self.ticker,
            "index": self.index,
        }
