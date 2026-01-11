class PreviousEarningsInformation:
    def __init__(self, expected_eps: float, actual_eps: float, price_diff: float):
        self._expected_eps = expected_eps
        self._actual_eps = actual_eps
        self._price_diff = price_diff

    @property
    def expected_eps(self) -> float:
        return self._expected_eps

    @property
    def actual_eps(self) -> float:
        return self._actual_eps

    @property
    def price_diff(self) -> float:
        return self._price_diff

    def to_dict(self) -> dict:
        return {
            "expected_eps": self._expected_eps,
            "actual_eps": self._actual_eps,
            "price_diff": self._price_diff,
        }
