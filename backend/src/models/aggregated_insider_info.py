class AggregatedInsiderInfo:
    """Class that represents a data model for aggregated insider information.

    Fields:
        ticker (str): Ticker of the company the insider info is about.
        bought (float): Amount of money for which the insiders bought stocks for this company.
        sold (float): Amount of money for which the insiders sold stocks for this company.
    """

    def __init__(self, ticker: str, bought: float, sold: float):
        self.__ticker = ticker
        self.__bought = bought if bought >= 0 else 0
        self.__sold = sold if sold >= 0 else 0

    @property
    def ticker(self) -> str:
        """Getter for the ticker of the filtered insider trading information."""
        return self.__ticker

    @property
    def bought(self) -> float:
        """Getter for the total value of bought insider trading information."""
        return self.__bought

    @property
    def sold(self) -> float:
        """Getter for the total value of sold insider trading information."""
        return self.__sold

    def to_dict(self) -> dict:
        """Convert FilteredInsiderInfo object to a dictionary."""
        return {
            "ticker": self.ticker,
            "bought": self.bought,
            "sold": self.sold,
        }
