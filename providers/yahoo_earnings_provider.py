from datetime import date, datetime, timedelta

import yfinance as yf

from models.earnings_information import EarningsInformation
from models.eps_information import EpsInformation
from models.previous_earnings_information import PreviousEarningsInformation
from providers.earnings_provider import EarningsProvider


class YahooEarningsProvider(EarningsProvider):
    """Class that is responsible for providing Earnigns information by using yahoo finance API."""

    def fetch_earnings(
        self, tickers: list[str], cutoff: datetime
    ) -> list[EarningsInformation]:
        """Return relevant Earnings report informtion for given companies.

        Args:
            tickers (list[str]): List of ticker for which to check if there is an upcoming earnings report.
            cutoff (datetime): How far into the future a report can't be to be included.

        Returns:
            list[EarningsInformation]: List of relevant earnings report inforation for given companies.
        """
        result: list[EarningsInformation] = []
        for ticker in tickers:
            try:
                stock = yf.Ticker(ticker)

                calendar = self._get_stock_calendar(stock)
                if not calendar:
                    continue

                earnings_date = self._get_earnings_date(calendar, cutoff)
                if earnings_date is None:
                    continue

                company_name = self._get_company_name(stock)
                market_cap = self._get_market_cap(stock)
                eps = self._get_eps(calendar)
                revenue = self._get_revenue(calendar)
                price_last_15_days = self._get_price_last_15_days(stock)
                prev_earnings = self._get_previous_earnings(stock)

                result.append(
                    EarningsInformation(
                        ticker=ticker,
                        name=company_name,
                        date=earnings_date,
                        market_cap=market_cap,
                        eps=eps,
                        revenue=revenue,
                        value_last_15_days=price_last_15_days,
                        previous_earnings=prev_earnings,
                    )
                )

            except Exception as e:
                print(f"Error fetching earnings for {ticker}: {e}")
                continue
        return result

    def _get_stock_calendar(self, stock: yf.Ticker) -> dict | None:
        """Get the stock calendar that conatins all usefull information."""
        try:
            calendar = stock.calendar
            return calendar
        except Exception as e:
            print(f"Error fetching calendar for stock: {e}")
            return None

    def _get_earnings_date(self, calendar: dict, cutoff: datetime) -> datetime | None:
        """Get the date of the first upcoming earnings report for a company.

        Returs a date only if it is sooner that cutoff time."""
        try:
            earnings_date = calendar.get("Earnings Date", None)[0]
            if earnings_date is None or not (
                datetime.today().date() <= earnings_date <= cutoff
            ):
                return None
            return earnings_date
        except Exception as e:
            print(f"Error fetching earnings date from calendar: {e}")
            return None

    def _get_company_name(self, stock: yf.Ticker) -> str:
        """Returns a name of the company based on ticker."""
        try:
            info = stock.info or {}
            company_name = info.get("shortName", "")
            return company_name
        except Exception as e:
            print(f"Error fetching company name: {e}")
            return ""

    def _get_market_cap(self, stock: yf.Ticker) -> int:
        """Returns the market cap of a company."""
        try:
            info = stock.info or {}
            market_cap = info.get("marketCap", 0)
            return market_cap
        except Exception as e:
            print(f"Error fetching market cap: {e}")
            return 0

    def _get_eps(self, calendar: dict) -> EpsInformation | None:
        """Returns EPS estimates for the next upcoming earnings report."""
        try:
            eps_avg = calendar.get("Earnings Average", None)
            eps_low = calendar.get("Earnings Low", None)
            eps_high = calendar.get("Earnings High", None)

            if eps_avg is not None and eps_low is not None and eps_high is not None:
                eps_info = EpsInformation(round(eps_avg, 2), eps_low, eps_high)
                return eps_info
            return None
        except Exception as e:
            print(f"Error fetching EPS information: {e}")
            return None

    def _get_revenue(self, calendar: dict) -> int:
        """Returns the revenue of the company."""
        try:
            revenue = calendar.get("Revenue Average", 0)
            return revenue
        except Exception as e:
            print(f"Error fetching revenue information: {e}")
            return 0

    def _get_price_last_15_days(self, stock: yf.Ticker) -> list[float]:
        """Returns the Closing price of a stock of the last 15 days."""
        try:
            hist = stock.history(period="15d")
            if not hist.empty:
                return hist["Close"].round(2).tolist()
            return []
        except Exception as e:
            print(f"Error fetching price history: {e}")
            return []

    def _get_previous_earnings(
        self, stock: yf.Ticker
    ) -> list[PreviousEarningsInformation]:
        """Returns EPS information about the last 4 earnings."""
        prev_earnings: list[PreviousEarningsInformation] = []
        try:
            earnings_history = stock.get_earnings_dates()
            if earnings_history is not None and not earnings_history.empty:
                last_5 = earnings_history.head(5)
                for edate, row in last_5.iterrows():
                    earnings_date = edate.date()
                    if earnings_date > date.today():
                        continue
                    hist = stock.history(
                        start=earnings_date - timedelta(days=5),
                        end=earnings_date + timedelta(days=6),
                    )
                    if not hist.empty:
                        price_before = hist.iloc[0]["Close"]
                        price_after = hist.iloc[-1]["Close"]
                        price_diff = (price_after - price_before) / price_before * 100
                    else:
                        price_diff = 0
                    prev_earnings.append(
                        PreviousEarningsInformation(
                            expected_eps=float(row.get("EPS Estimate", 0.0)),
                            actual_eps=float(row.get("Reported EPS", 0.0)),
                            price_diff=float(price_diff),
                        )
                    )
            return prev_earnings
        except Exception as e:
            print(f"Error fetching previous earnings information: {e}")
            return prev_earnings
