class EpsInformation:
    """Class that represents needed Earnings Per Share information."""

    def __init__(self, avg: float, low: float, high: float):
        self.__avg = avg
        self.__low = low
        self.__high = high

    @property
    def avg(self) -> float:
        """Getter for average estimated EPS."""
        return self.__avg

    @property
    def low(self) -> float:
        """Getter for low estimated EPS."""
        return self.__low

    @property
    def high(self) -> float:
        """Getter for high estimated EPS."""
        return self.__high

    def to_dict(self) -> dict:
        """Convert EPS information to dictionary."""
        return {
            "avg": self.__avg,
            "low": self.__low,
            "high": self.__high,
        }
