class EpsInformation:
    def __init__(self, avg: float, low: float, high: float):
        self._avg = avg
        self._low = low
        self._high = high

    @property
    def avg(self) -> float:
        return self._avg

    @property
    def low(self) -> float:
        return self._low

    @property
    def high(self) -> float:
        return self._high

    def to_dict(self) -> dict:
        return {
            "avg": self._avg,
            "low": self._low,
            "high": self._high,
        }
