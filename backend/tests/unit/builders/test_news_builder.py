from models.news_article import NewsArticle
from report_building.news_builder import NewsBuilder
from utils.enums.language import Language
from utils.localization import Localization


class TestNewsBuilder:
    """Test class for news builder tests."""

    def test__build_markdown_news_articled__md_string_returned(
        self, create_news_info: list[NewsArticle]
    ):
        """Check if build markdown returns a correct md string when correct data is given."""
        loc = Localization(Language.ENGLISH)
        news_builder = NewsBuilder(loc)
        md_string = news_builder.build_markdown(create_news_info)

        assert loc.translate("news_title") in md_string
        assert loc.translate("news_intro") in md_string

        for article in create_news_info:
            assert article.title in md_string

    def test__build_markdown_no_data__md_string_no_news(self):
        """Check if build markdown returns a md string with no news when no news are given."""
        loc = Localization(Language.ENGLISH)
        news_builder = NewsBuilder(loc)
        md_string = news_builder.build_markdown([])

        assert loc.translate("news_title") in md_string
        assert loc.translate("news_intro") in md_string
        assert loc.translate("news_date") not in md_string
