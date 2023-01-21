from terminal.pluglets.tile_grid.util import tile_grid
import pytest


class TestTileGridPluglet():

    def test_no_input(self):
        macro_output = tile_grid()
        assert "USAGE" in macro_output

    @pytest.mark.parametrize("bad_input", [
        pytest.param(
            None, id="null_input"
        ),
        pytest.param(
            {}, id="empty_dict_input"
        ),
        pytest.param(
            [], id="list_input"
        ),
        pytest.param(
            "tiles", id="string_input"
        )
    ])
    def test_bad_input(self, bad_input):
        macro_output = tile_grid()
        assert "USAGE" in macro_output
