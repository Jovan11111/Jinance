from models.news_article import NewsArticle
from report_building.report_builder import ReportBuilder


class NewsBuilder(ReportBuilder):
    """Class responsible for building the part of the report that conatins relevant news information in a .md format."""

    def __init__(self):
        print("NewsBuilder initialized")

    def build_markdown(self, news_data: list[NewsArticle]) -> str:
        """Returns .md formated report part that includes all given news information.

        Args:
            news_data (list[NewsArticle]): Information about relevant news articles that needs to be represented.

        Returns:
            str: String that contains all information in a formated way.
        """
        md: list[str] = []

        md.append("## Najbitnije vesti\n")
        md.append(
            "Ovo je automatski generisan izveštaj o najbitnijim vestima vezanim za "
            "finansijska tržišta objavljenim u prethodna 24 sata.\n"
        )

        for article in news_data:
            md.append(f"### [{article.title}]({article.url}) - {article.ticker}\n")
            md.append(f"Objavljeno: {article.pub_time.strftime('%d.%m.%Y %H:%M')}\n")
            md.append(f"{article.summary}\n")
            md.append("---\n")

        return "\n".join(md)
