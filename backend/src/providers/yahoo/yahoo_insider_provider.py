import logging

import yfinance as yf

from models.insider_information import InsiderInformation
from providers.insider_provider import InsiderProvider
from utils.enums.trade_type import TradeType

logger = logging.getLogger(__name__)


class YahooInsiderProvider(InsiderProvider):
    """Class that provides data about insider trading by using yahoo finance API."""

    def fetch_insider_trades(self, tickers: list[str]) -> list[InsiderInformation]:
        """Get all insider trades posted on yahoo finance.

        Args:
            tickers (list[str]): Tickers for which to check insider trades.

        Returns:
            list[InsiderInformation]: List of relevant insider trading information.
        """
        logger.debug("Fetching all insider information by using Yahoo Finance API.")

        insider_info: list[InsiderInformation] = []
        for ticker in tickers:
            try:
                stock = yf.Ticker(ticker)
                all_insider_info = stock.get_insider_transactions().to_dict(
                    orient="records"
                )
                for row in all_insider_info:
                    if not row["Text"]:
                        continue
                    insider_info.append(
                        InsiderInformation(
                            ticker=ticker,
                            value=row["Value"],
                            type=(
                                TradeType.GIFT
                                if row["Value"] == 0
                                else (
                                    TradeType.BUY
                                    if "Purchase" in row["Text"]
                                    else TradeType.SELL
                                )
                            ),
                            date=row["Start Date"],
                        )
                    )
            except Exception as e:
                logger.warning(f"Error fetching previous earnings information: {e}")
                continue
        return insider_info
