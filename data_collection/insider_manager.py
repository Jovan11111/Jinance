from datetime import date, datetime, timedelta
from pprint import pprint
import yfinance as yf
from utils import constants
from utils.singleton_meta import SingletonMeta


class InsiderManager(metaclass=SingletonMeta):
    def __init__(self, days_behind = 30, tickers = constants.TICKERS_SP_10):
        print("Initializing InsiderManager")
        self.insiders = []
        self.tickers = tickers
        self.days_behind = days_behind

    def get_insider_trading_data(self, number_of_companies):
        result = {}
        for ticker in self.tickers:
            if len(result) >= number_of_companies:
                break
            
            try:
                stock = yf.Ticker(ticker)
                cutoff = datetime.now() - timedelta(days=30)
                #print("PURCHASES")
                #print(stock.get_insider_purchases())
                print("TRANSACTIONS")
                last_30_days = []
                pprint(stock.get_insider_transactions().to_dict(orient="records"))
                for row in stock.get_insider_transactions().to_dict(orient="records"):
                    if row['Start Date'] >= cutoff:
                        last_30_days.append(row)
                print("--------------------")
                pprint(last_30_days)
                #print("ROSTER HOLDERS") 
                #print(stock.get_insider_roster_holders())
                break
            except Exception as e:
                print(f"{ticker}: {e}")
                continue
