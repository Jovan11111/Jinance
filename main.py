from data_collection.insider_manager import InsiderManager
from data_collection.news_manager import NewsManager
from jinance import Jinance


def main():
    pdf_path = Jinance.get_instance().generate_report(number_of_companies=5)
    print(f"PDF report written to: {pdf_path}")


if __name__ == "__main__":
    news_manager = NewsManager.get_instance()
    news_manager.get_latest_news()
    #main()
