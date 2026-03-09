class InsiderInformation:
    """Class that represents information about insider trading that is in the report."""

    def __init__(
        self,
        ticker: str,
        amount_bought: int,
        amount_sold: int,
        buyers: list[str],
        sellers: list[str],
    ):
        self._ticker: str = ticker
        self._amount_bought: int = amount_bought
        self._amount_sold: int = amount_sold
        self._buyers: list[str] = buyers
        self._sellers: list[str] = sellers

    @property
    def ticker(self) -> str:
        """Getter for the ticker of the insider trading information."""
        return self._ticker

    @property
    def amount_bought(self) -> int:
        """Getter for the amount bought in the insider trading information."""
        return self._amount_bought

    @property
    def amount_sold(self) -> int:
        """Getter for the amount sold in the insider trading information."""
        return self._amount_sold

    @property
    def buyers(self) -> list[str]:
        """Getter for the list of buyers in the insider trading information."""
        return self._buyers

    @property
    def sellers(self) -> list[str]:
        """Getter for the list of sellers in the insider trading information."""
        return self._sellers

    def to_dict(self) -> dict:
        """Convert InsiderInformation object to a dictionary."""
        return {
            "ticker": self.ticker,
            "amount_bought": self.amount_bought,
            "amount_sold": self.amount_sold,
            "buyers": self.buyers,
            "sellers": self.sellers,
        }
