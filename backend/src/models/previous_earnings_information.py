class PreviousEarningsInformation:
    """Class that represents relevant information about previous earnings report.

    Fields:
        expected_eps (float): EPS that was expected for that earnings.
        actual_eps (float): Actual EPS that was published for that earnings.
        price_diff (float): How much the price changed between 5 days before and 10 days after the earnings.
    """

    def __init__(self, expected_eps: float, actual_eps: float, price_diff: float):
        self.__expected_eps = expected_eps
        self.__actual_eps = actual_eps
        self.__price_diff = round(price_diff, 2)

    @property
    def expected_eps(self) -> float:
        """Getter for expected eps of the earnings report."""
        return self.__expected_eps

    @property
    def actual_eps(self) -> float:
        """Getter for actual eps of the earnings report"""
        return self.__actual_eps

    @property
    def price_diff(self) -> float:
        """Getter for how much the price changed between 5 days before the report, and 10 days after the report."""
        return self.__price_diff

    def to_dict(self) -> dict:
        """Converts PreviousEarningsInformation object to dictionary."""
        return {
            "expected_eps": self.__expected_eps,
            "actual_eps": self.__actual_eps,
            "price_diff": self.__price_diff,
        }
