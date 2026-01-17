from models.news_article import NewsArticle
from report_building.report_builder import ReportBuilder


class NewsBuilder(ReportBuilder):
    def __init__(self):
        print("NewsBuilder initialized")

    def build_markdown(self, news_data: list[NewsArticle]) -> str:
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
