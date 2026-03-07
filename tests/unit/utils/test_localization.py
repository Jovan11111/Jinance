from utils.enums.language import Language
from utils.localization import Localization


class TestLocalization:
    """Class for test for localizatio class"""

    def test__serbian__translates_to_serbian(self):
        """Check if Localization class correctly translates to Serbian"""
        localization = Localization(Language.SERBIAN)
        assert localization.translate("report_title") == "Jinance izveštaj za"
        assert localization.translate("earnings_title") == "Earnings izveštaj"
        assert (
            localization.translate("earnings_intro")
            == "Ovo je automatski generisan izveštaj o nadolazećim javnim objavama prihoda, u kom su prikazani osnovni podaci o narednim firmama koje će javno objaviti prihode."
        )
        assert localization.translate("earnings_date") == "Datum earnings-a:"
        assert localization.translate("earnings_eps_avg") == "Prosečna EPS:"
        assert localization.translate("earnings_eps_low") == "Pesimistična EPS:"
        assert localization.translate("earnings_eps_high") == "Optimistična EPS:"
        assert localization.translate("earnings_prev_eps") == "Prethodni EPS"
        assert localization.translate("earnings_latest") == "najskoriji"
        assert localization.translate("earnings_oldest") == "najstariji"
        assert localization.translate("earnings_prev_eps_expected") == "Očekivani"
        assert localization.translate("earnings_prev_eps_actual") == "Stvarni"
        assert localization.translate("earnings_prev_eps_diff") == "Promena cene (%)"
        assert localization.translate("earnings_market_cap") == "Vrednost firme:"
        assert localization.translate("earnings_revenue") == "Prihod firme:"
        assert (
            localization.translate("earnings_price_chart")
            == "Cena akcije poslednjih 15 dana:"
        )
        assert localization.translate("news_title") == "Najbitnije vesti"
        assert (
            localization.translate("news_intro")
            == "Ovo je automatski generisan izveštaj o najbitnijim vestima vezanim za finansijsko tržište"
        )
        assert localization.translate("news_date") == "Objavljeno:"
        assert (
            localization.translate("price_perf_title")
            == "Izveštaj o najboljim i najgorim performansama cena akcija"
        )
        assert (
            localization.translate("price_perf_intro")
            == "Ovo je automatski generisan izveštaj o najboljim i najgorim performansama cena akcija na berzi."
        )
        assert (
            localization.translate("price_perf_best")
            == "Najbolje performanse cena akcija"
        )
        assert localization.translate("price_perf_old_price") == "Cena pre 6 meseci:"
        assert localization.translate("price_perf_cur_price") == "Trenutna cena:"
        assert localization.translate("price_perf_change") == "Promena cene (%):"
        assert (
            localization.translate("price_perf_worst")
            == "Najgore performanse cena akcija"
        )
        assert localization.translate("graph_days") == "Dani"
        assert localization.translate("graph_price") == "Cena (USD)"

    def test__english__translates_to_english(self):
        """Check if Localization class correctly translates to English"""
        localization = Localization(Language.ENGLISH)
        assert localization.translate("report_title") == "Jinance report for"
        assert localization.translate("earnings_title") == "Earnings report"
        assert (
            localization.translate("earnings_intro")
            == "This is an automatically generated report on upcoming earnings announcements, where basic information about the next companies that will publicly announce earnings is displayed."
        )
        assert localization.translate("earnings_date") == "Earnings date:"
        assert localization.translate("earnings_eps_avg") == "Average EPS:"
        assert localization.translate("earnings_eps_low") == "Pessimistic EPS:"
        assert localization.translate("earnings_eps_high") == "Optimistic EPS:"
        assert localization.translate("earnings_prev_eps") == "Previous EPS"
        assert localization.translate("earnings_latest") == "latest"
        assert localization.translate("earnings_oldest") == "oldest"
        assert localization.translate("earnings_prev_eps_expected") == "Expected"
        assert localization.translate("earnings_prev_eps_actual") == "Actual"
        assert localization.translate("earnings_prev_eps_diff") == "Price Change (%)"
        assert localization.translate("earnings_market_cap") == "Company Value:"
        assert localization.translate("earnings_revenue") == "Company Revenue:"
        assert (
            localization.translate("earnings_price_chart")
            == "Stock Price Last 15 Days:"
        )
        assert localization.translate("news_title") == "Most important news"
        assert (
            localization.translate("news_intro")
            == "This is an automatically generated report on the most important news related to the stock market"
        )
        assert localization.translate("news_date") == "Published:"
        assert (
            localization.translate("price_perf_title")
            == "Report on the best and worst stock price performances"
        )
        assert (
            localization.translate("price_perf_intro")
            == "This is an automatically generated report on the best and worst stock price performances on the stock market."
        )
        assert (
            localization.translate("price_perf_best") == "Best stock price performances"
        )
        assert localization.translate("price_perf_old_price") == "Price 6 months ago:"
        assert localization.translate("price_perf_cur_price") == "Current Price:"
        assert localization.translate("price_perf_change") == "Price Change (%):"
        assert (
            localization.translate("price_perf_worst")
            == "Worst stock price performances"
        )
        assert localization.translate("graph_days") == "Days"
        assert localization.translate("graph_price") == "Price (USD)"

    def test__nonexistent_key_returns_empty_string(self):
        """Check if Localization returns empty string for nonexistent key"""
        localization_sr = Localization(Language.SERBIAN)
        localization_en = Localization(Language.ENGLISH)

        assert localization_sr.translate("nonexistent") == ""
        assert localization_en.translate("nonexistent") == ""
