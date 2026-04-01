from datetime import date

from models.section_data import SectionData
from report_building.report_builder_director import ReportBuilderDirector
from utils.enums.language import Language


class TestReportBuilderDirector:
    """Test class for report builder director tests."""

    def test__create_pdf_report__creates_pdf_report(
        self, create_section_data: list[SectionData], mock_earnings_section
    ):
        """Check if calling create_pdf_report actually crates a pdf report on a returned path."""
        report_builder = ReportBuilderDirector(Language.ENGLISH)

        file_path = report_builder.create_pdf_report([create_section_data])
        today_str = date.today().strftime("%Y%m%d")

        assert f"report_{today_str}.pdf" in file_path
        # assert os.path.exists(file_path)
        # os.remove(file_path)

    def test__create_pdf_report_no_data__creates_pdf_report(self):
        """Check if calling create_pdf_report actually creates a pdf report on a returnes path."""
        report_builder = ReportBuilderDirector(Language.ENGLISH)

        file_path = report_builder.create_pdf_report([])
        today_str = date.today().strftime("%Y%m%d")

        assert f"report_{today_str}.pdf" in file_path
        # assert os.path.exists(file_path)
        # os.remove(file_path)
