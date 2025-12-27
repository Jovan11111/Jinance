from jinance import Jinance


def main():
    pdf_path = Jinance.get_instance().generate_report(number_of_companies=5)
    print(f"PDF report written to: {pdf_path}")


if __name__ == "__main__":
    main()
