import datetime


class NewsArticle:
    """Class that represents information about News articles that are in the report."""

    def __init__(
        self, title: str, summary: str, pub_time: datetime, url: str, ticker: str
    ):
        self._title: str = title
        self._summary: str = summary
        self._pub_time: datetime = pub_time
        self._url: str = url
        self._ticker: str = ticker

    @property
    def title(self) -> str:
        """Getter for the title of the article."""
        return self._title

    @property
    def summary(self) -> str:
        """Getter for the summary of the article"""
        return self._summary

    @property
    def pub_time(self) -> datetime:
        """Getter for the publish time of the article"""
        return self._pub_time

    @property
    def url(self) -> str:
        """Getter for the url to the article"""
        return self._url

    @property
    def ticker(self) -> str:
        """Getter for a ticker that is most relevant to the article"""
        return self._ticker

    def to_dict(self) -> dict:
        """Convert NewsArticle object to a dictionary."""
        return {
            "title": self._title,
            "summary": self._summary,
            "pub_time": self._pub_time.isoformat(),
            "url": self._url,
            "ticker": self._ticker,
        }
