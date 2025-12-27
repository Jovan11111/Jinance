import pprint
import yfinance as yf
from datetime import date, datetime, timedelta

import utils.constants as constants
from utils.singleton_meta import SingletonMeta

class EarningsManager(metaclass=SingletonMeta):
    """Fetch upcoming earnings."""

    def __init__(self, days_ahead=30, tickers = constants.TICKERS_SP_100):
        print("EarningsManager initialized")
        self.days_ahead = days_ahead
        self.tickers = tickers

    def get_latest_upcoming_earnings(self, number_of_companies):
        result = {}
        today = datetime.today().date()
        cutoff = today + timedelta(days=self.days_ahead)

        for ticker in self.tickers:
            if len(result) >= number_of_companies:
                break

            try:
                stock = yf.Ticker(ticker)
                calendar = stock.calendar
                
                if calendar is None or len(calendar) == 0:
                    continue

                earnings_date = calendar.get("Earnings Date", [None])[0]
                if earnings_date is None or not (today <= earnings_date <= cutoff):
                    continue

                # --- DEFAULT VALUES ---
                company_name = ""
                market_cap = 0
                eps = []
                revenue = 0
                price_last_15_days = []
                prev_earnings = []

                # --- COMPANY INFO ---
                info = stock.info or {}
                company_name = info.get("shortName", "")
                market_cap = info.get("marketCap", 0)

                # --- EPS ---
                eps_avg = calendar.get("Earnings Average", None)
                eps_low = calendar.get("Earnings Low", None)
                eps_high = calendar.get("Earnings High", None)

                if eps_avg is not None and eps_low is not None and eps_high is not None:
                    eps = [round(eps_avg, 2), eps_low, eps_high]

                # --- REVENUE ---
                revenue = calendar.get("Revenue Average", 0)

                # --- PRICE LAST 15 DAYS ---
                hist = stock.history(period="15d")
                if not hist.empty:
                    price_last_15_days = hist["Close"].round(2).tolist()

                # --- PREVIOUS EARNINGS ---
                earnings_history = stock.get_earnings_dates()
                if earnings_history is not None and not earnings_history.empty:
                    last_5 = earnings_history.head(5)
                    for edate, row in last_5.iterrows():
                        earnings_date = edate.date()
                        if earnings_date > date.today():
                            continue
                        hist = stock.history(start=earnings_date - timedelta(days=5), end=earnings_date + timedelta(days=6)) 
                        if not hist.empty:
                            price_before = hist.iloc[0]["Close"]
                            price_after = hist.iloc[-1]["Close"]
                            price_diff = (price_after - price_before) / price_before * 100
                        else:
                            price_diff = 0
                        prev_earnings.append({
                            "expected_eps": float(row.get("EPS Estimate", 0.0)),
                            "actual_eps": float(row.get("Reported EPS", 0.0)),
                            "price_diff": float(price_diff)
                        })

                result[ticker] = {
                    "name": company_name,
                    "value_last_15_days": price_last_15_days,
                    "market_cap": market_cap,
                    "eps": eps,
                    "date": earnings_date,
                    "revenue": revenue,
                    "previous_earnings": prev_earnings
                }

            except Exception as e:
                print(f"{ticker}: {e}")
                continue

        return result
