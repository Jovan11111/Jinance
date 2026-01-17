class EpsInformation:
    """Class that represents needed Earnings Per Share information."""

    def __init__(self, avg: float, low: float, high: float):
        self._avg = avg
        self._low = low
        self._high = high

    @property
    def avg(self) -> float:
        """Getter for average estimated EPS."""
        return self._avg

    @property
    def low(self) -> float:
        """Getter for low estimated EPS."""
        return self._low

    @property
    def high(self) -> float:
        """Getter for high estimated EPS."""
        return self._high

    def to_dict(self) -> dict:
        """Convert EPS information to dictionary."""
        return {
            "avg": self._avg,
            "low": self._low,
            "high": self._high,
        }
