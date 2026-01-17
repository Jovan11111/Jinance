import datetime


class NewsArticle:
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
        return self._title

    @property
    def summary(self) -> str:
        return self._summary

    @property
    def pub_time(self) -> datetime:
        return self._pub_time

    @property
    def url(self) -> str:
        return self._url

    @property
    def ticker(self) -> str:
        return self._ticker

    def to_dict(self) -> dict:
        return {
            "title": self._title,
            "summary": self._summary,
            "pub_time": self._pub_time.isoformat(),
            "url": self._url,
            "ticker": self._ticker,
        }
