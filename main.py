import logging

from jinance import Jinance

logger = logging.getLogger(__name__)


def main():
    pdf_path = Jinance.get_instance().generate_report(number_of_companies=5)
    logger.info(f"PDF report written to: {pdf_path}")


if __name__ == "__main__":
    main()
