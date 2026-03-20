import os
import shutil
from pathlib import Path

from report_building.graph_builder import GraphBuilder
from utils.enums.language import Language
from utils.localization import Localization


class TestGraphBuilder:
    """Test class for Graph builder tests."""

    def test__build_graph_detailed__path_returned_pictures_exists(self):
        """Check if build price graph actually creates pictures in the given folder, wether they are detailed or not, and deletes old files in graphs dir."""
        existing_file = Path("graphs").joinpath("some_file")
        existing_file.parent.mkdir(parents=True, exist_ok=True)
        existing_file.touch()
        graph_builder = GraphBuilder(Localization(Language.ENGLISH), "graphs")
        assert not os.path.exists(existing_file)

        file_path_det = graph_builder.build_price_graph([i for i in range(20)], "TCK1")
        assert "graphs" in file_path_det
        assert "TCK1" in file_path_det
        assert "png" in file_path_det

        file_path_non_det = graph_builder.build_price_graph(
            [i for i in range(25)], "TCK2"
        )
        assert "graphs" in file_path_non_det
        assert "TCK2" in file_path_non_det
        assert "png" in file_path_non_det

        assert os.path.exists(file_path_det)
        assert os.path.exists(file_path_non_det)

        shutil.rmtree("graphs", ignore_errors=True)
        del graph_builder


