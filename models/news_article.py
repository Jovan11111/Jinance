import datetime


class NewsArticle:
    def __init__(self, title: str, summary: str, pubDate: datetime, url: str):
        self._title: str = title
        self._summary: str = summary
        self._pubDate: datetime = pubDate
        self._url: str = url

    @property
    def title(self) -> str:
        return self._title

    @property
    def summary(self) -> str:
        return self._summary

    @property
    def pubDate(self) -> datetime:
        return self._pubDate

    @property
    def url(self) -> str:
        return self._url

    def to_dict(self) -> dict:
        return {
            "title": self._title,
            "summary": self._summary,
            "pubDate": self._pubDate.isoformat(),
            "url": self._url,
        }
