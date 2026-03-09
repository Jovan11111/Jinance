import logging

from models.insider_information import InsiderInformation
from providers.insider_provider import InsiderProvider

logger = logging.getLogger(__name__)


class YahooInsiderProvider(InsiderProvider):
    """Class that provides data about insider trading by using yahoo finance API."""

    def fetch_insider_trades(
        self, tickers: list[str], days_behind: int
    ) -> list[InsiderInformation]:
        """Get all insider trades posted on yahoo finance in the last {days_behind} days.

        Args:
            tickers (list[str]): Tickers for which to check insider trades
            days_behind (int): How old can an insider trade be to be included

        Returns:
            list[InsiderInformation]: List of relevant insider trading information.
        """

        return []


"""
def get_insider_trading_data(self, number_of_companies):
        result = {}
        for ticker in self.tickers:
            if len(result) >= number_of_companies:
                break

            try:
                stock = yf.Ticker(ticker)
                cutoff = datetime.now() - timedelta(days=30)
                # print("PURCHASES")
                # print(stock.get_insider_purchases())
                print("TRANSACTIONS")
                last_30_days = []
                pprint(stock.get_insider_transactions().to_dict(orient="records"))
                for row in stock.get_insider_transactions().to_dict(orient="records"):
                    if row["Start Date"] >= cutoff:
                        last_30_days.append(row)
                print("--------------------")
                pprint(last_30_days)
                # print("ROSTER HOLDERS")
                # print(stock.get_insider_roster_holders())
                break
            except Exception as e:
                print(f"{ticker}: {e}")
                continue

"""
