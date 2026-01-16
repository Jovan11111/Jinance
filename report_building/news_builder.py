from models.news_article import NewsArticle
from report_building.report_builder_director import ReportBuilder


class NewsBuilder(ReportBuilder):
    def __init__(self, news_data: list[NewsArticle]):
        self.news_data = news_data

    def build_markdown(self) -> str:
        md = []
        return "\n".join(md)
