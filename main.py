from jinance import Jinance
from managers.news_manager import NewsManager


def main():
    pdf_path = Jinance.get_instance().generate_report(number_of_companies=5)
    print(f"PDF report written to: {pdf_path}")


if __name__ == "__main__":
    news_manager = NewsManager.get_instance()
    news_manager.get_latest_news()
    # main()
