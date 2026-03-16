from datetime import datetime


class NewsArticle:
    """Class that represents information about News articles that are in the report.

    Fields:
        ticker (str): Ticker of the company the article is about.
        title (str): Title of the article.
        summary (str): Summary of the article.
        pub_time (datetime): Time at which the article was published.
        url (str): Link to the article.
    """

    def __init__(
        self, title: str, summary: str, pub_time: datetime, url: str, ticker: str
    ):
        self.__title: str = title
        self.__summary: str = summary
        self.__pub_time: datetime = pub_time
        self.__url: str = url
        self.__ticker: str = ticker

    @property
    def title(self) -> str:
        """Getter for the title of the article."""
        return self.__title

    @property
    def summary(self) -> str:
        """Getter for the summary of the article"""
        return self.__summary

    @property
    def pub_time(self) -> datetime:
        """Getter for the publish time of the article"""
        return self.__pub_time

    @property
    def url(self) -> str:
        """Getter for the url to the article"""
        return self.__url

    @property
    def ticker(self) -> str:
        """Getter for a ticker that is most relevant to the article"""
        return self.__ticker

    def to_dict(self) -> dict:
        """Convert NewsArticle object to a dictionary."""
        return {
            "title": self.__title,
            "summary": self.__summary,
            "pub_time": self.__pub_time.isoformat() if self.pub_time else "",
            "url": self.__url,
            "ticker": self.__ticker,
        }
