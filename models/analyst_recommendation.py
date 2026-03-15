class AnalystRecommendation:
    """Class that represents the data model for Analyst recommendation.

    Fields:
        ticker (str): Ticker of the company the recommendation is about.
        index (float): number between -100 and 100, where -100 means strong sell, and 100 means strong buy.
    """

    def __init__(self, ticker: str, index: float):
        self.__ticker = ticker
        self.__index = index if index >= -100 and index <= 100 else 0

    @property
    def ticker(self) -> str:
        """Getter for the ticker of the analyst recommendation information."""
        return self.__ticker

    @property
    def index(self) -> float:
        """Getter for the index of the analyst recommendation information."""
        return self.__index

    def to_dict(self) -> dict:
        """Convert AnalystRecommendation object to a dictionary."""
        return {
            "ticker": self.ticker,
            "index": self.index,
        }
