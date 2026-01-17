class PreviousEarningsInformation:
    """Class that represents releavnt information about previos earnings report."""

    def __init__(self, expected_eps: float, actual_eps: float, price_diff: float):
        self._expected_eps = expected_eps
        self._actual_eps = actual_eps
        self._price_diff = round(price_diff, 2)

    @property
    def expected_eps(self) -> float:
        """Getter for expected eps of the earnings report."""
        return self._expected_eps

    @property
    def actual_eps(self) -> float:
        """Getter for actual eps of the earnings report"""
        return self._actual_eps

    @property
    def price_diff(self) -> float:
        """Getter for how much the price changed between 5 days before the report, and 10 days after the report."""
        return self._price_diff

    def to_dict(self) -> dict:
        """Converts PreviousEarningsInformation object to dictionary."""
        return {
            "expected_eps": self._expected_eps,
            "actual_eps": self._actual_eps,
            "price_diff": self._price_diff,
        }
