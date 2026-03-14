from utils.enums.language import Language


class Localization:
    def __init__(self, language: Language):
        self.__language = language
        self.__translations = {
            # Report builder director localization
            "report_title": {
                Language.SERBIAN: "Jinance izveštaj za",
                Language.ENGLISH: "Jinance report for",
            },
            # Earnings report builder localization
            "earnings_title": {
                Language.SERBIAN: "Earnings izveštaj",
                Language.ENGLISH: "Earnings report",
            },
            "earnings_intro": {
                Language.SERBIAN: "Ovo je automatski generisan izveštaj o nadolazećim javnim objavama prihoda, u kom su prikazani osnovni podaci o narednim firmama koje će javno objaviti prihode.",
                Language.ENGLISH: "This is an automatically generated report on upcoming earnings announcements, where basic information about the next companies that will publicly announce earnings is displayed.",
            },
            "earnings_date": {
                Language.SERBIAN: "Datum earnings-a:",
                Language.ENGLISH: "Earnings date:",
            },
            "earnings_eps_avg": {
                Language.SERBIAN: "Prosečna EPS:",
                Language.ENGLISH: "Average EPS:",
            },
            "earnings_eps_low": {
                Language.SERBIAN: "Pesimistična EPS:",
                Language.ENGLISH: "Pessimistic EPS:",
            },
            "earnings_eps_high": {
                Language.SERBIAN: "Optimistična EPS:",
                Language.ENGLISH: "Optimistic EPS:",
            },
            "earnings_prev_eps": {
                Language.SERBIAN: "Prethodni EPS",
                Language.ENGLISH: "Previous EPS",
            },
            "earnings_latest": {
                Language.SERBIAN: "najskoriji",
                Language.ENGLISH: "latest",
            },
            "earnings_oldest": {
                Language.SERBIAN: "najstariji",
                Language.ENGLISH: "oldest",
            },
            "earnings_prev_eps_expected": {
                Language.SERBIAN: "Očekivani",
                Language.ENGLISH: "Expected",
            },
            "earnings_prev_eps_actual": {
                Language.SERBIAN: "Stvarni",
                Language.ENGLISH: "Actual",
            },
            "earnings_prev_eps_diff": {
                Language.SERBIAN: "Promena cene (%)",
                Language.ENGLISH: "Price Change (%)",
            },
            "earnings_market_cap": {
                Language.SERBIAN: "Vrednost firme:",
                Language.ENGLISH: "Company Value:",
            },
            "earnings_revenue": {
                Language.SERBIAN: "Prihod firme:",
                Language.ENGLISH: "Company Revenue:",
            },
            "earnings_price_chart": {
                Language.SERBIAN: "Cena akcije poslednjih 15 dana:",
                Language.ENGLISH: "Stock Price Last 15 Days:",
            },
            # News report builder localization
            "news_title": {
                Language.SERBIAN: "Najbitnije vesti",
                Language.ENGLISH: "Most important news",
            },
            "news_intro": {
                Language.SERBIAN: "Ovo je automatski generisan izveštaj o najbitnijim vestima vezanim za finansijsko tržište",
                Language.ENGLISH: "This is an automatically generated report on the most important news related to the stock market",
            },
            "news_date": {
                Language.SERBIAN: "Objavljeno:",
                Language.ENGLISH: "Published:",
            },
            # Price performance report builder localization
            "price_perf_title": {
                Language.SERBIAN: "Izveštaj o najboljim i najgorim performansama cena akcija",
                Language.ENGLISH: "Report on the best and worst stock price performances",
            },
            "price_perf_intro": {
                Language.SERBIAN: "Ovo je automatski generisan izveštaj o najboljim i najgorim performansama cena akcija na berzi.",
                Language.ENGLISH: "This is an automatically generated report on the best and worst stock price performances on the stock market.",
            },
            "price_perf_best": {
                Language.SERBIAN: "Najbolje performanse cena akcija",
                Language.ENGLISH: "Best stock price performances",
            },
            "price_perf_old_price": {
                Language.SERBIAN: "Cena pre 6 meseci:",
                Language.ENGLISH: "Price 6 months ago:",
            },
            "price_perf_cur_price": {
                Language.SERBIAN: "Trenutna cena:",
                Language.ENGLISH: "Current Price:",
            },
            "price_perf_change": {
                Language.SERBIAN: "Promena cene (%):",
                Language.ENGLISH: "Price Change (%):",
            },
            "price_perf_worst": {
                Language.SERBIAN: "Najgore performanse cena akcija",
                Language.ENGLISH: "Worst stock price performances",
            },
            # Insider report builder localization
            "insider_title": {
                Language.SERBIAN: "Insider izveštaj",
                Language.ENGLISH: "Insider trading report",
            },
            "insider_intro": {
                Language.SERBIAN: "Pregled najvećih kupaca i prodavaca insajderskih transakcija.",
                Language.ENGLISH: "Overview of the biggest insider buyers and sellers.",
            },
            "insider_buyers": {
                Language.SERBIAN: "Najveći kupci",
                Language.ENGLISH: "Top buyers",
            },
            "insider_sellers": {
                Language.SERBIAN: "Najveći prodavci",
                Language.ENGLISH: "Top sellers",
            },
            "insider_ticker": {
                Language.SERBIAN: "Tiker",
                Language.ENGLISH: "Ticker",
            },
            "insider_amount_sold": {
                Language.SERBIAN: "Iznos prodaje",
                Language.ENGLISH: "Amount sold",
            },
            "insider_amount_bought": {
                Language.SERBIAN: "Iznos kupovine",
                Language.ENGLISH: "Amount bought",
            },
            # Analyst recommendations report builder localization
            "analyst_title": {
                Language.SERBIAN: "Preporuke analitičara",
                Language.ENGLISH: "Analyst recommendations",
            },
            "analyst_intro": {
                Language.SERBIAN: "Ovo je automatski generisan izveštaj o preporukama analitičara. Preporuka analitičara se meri indeksom koji ima vrednosti od -100 (jaka preporuka na prodaju) do 100 (jaka preporuka na kupovanje)",
                Language.ENGLISH: "This is an automatically generated report on analyst recommendations. Analyst recommendation is measured by an index that has values from -100 (strong sell recommendation) to 100 (strong buy recommendation)",
            },
            "analyst_sells": {
                Language.SERBIAN: "Najjače preporuke na prodaju",
                Language.ENGLISH: "Strongest Sell Recommendations",
            },
            "analyst_buys": {
                Language.SERBIAN: "Najjače preporuke na kupovanje",
                Language.ENGLISH: "Strongest Buy Recommendations",
            },
            "analyst_ticker": {
                Language.SERBIAN: "Tiker",
                Language.ENGLISH: "Ticker",
            },
            "analyst_index": {
                Language.SERBIAN: "Indeks preporuke",
                Language.ENGLISH: "Recommendation Index",
            },
            # Graph builder localization
            "graph_days": {Language.SERBIAN: "Dani", Language.ENGLISH: "Days"},
            "graph_price": {
                Language.SERBIAN: "Cena (USD)",
                Language.ENGLISH: "Price (USD)",
            },
        }

    def translate(self, key: str) -> str:
        """Translate a given key to a selected language.

        Args:
            key (str): key that is being translated.

        Returns:
            str: Translated string in the selected language. If the key doesn't exist, return empty string.
        """
        if key not in self.__translations:
            return ""
        return self.__translations[key][self.__language]
