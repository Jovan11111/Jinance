from enum import Enum


class SectionType(Enum):
    """Enumeration that shows which part of the report the section is about.

    Types:
        EARNINGS: Earnings section.
        NEWS: Latest news section.
        PRICE_PERFORMANCE: Price performance section.
        INSIDER_TRADES: Insider trading section.
        ANALYST_RATINGS: Analyst recommendations section.
    """

    EARNINGS = "earnings"
    NEWS = "news"
    PRICE_PERFORMANCE = "price_performance"
    INSIDER_TRADES = "insider_trades"
    ANALYST_RATINGS = "analyst_ratings"
