from terminal.pluglets.tile_grid.util import tile_grid
import pytest


class TestTileGridPluglet():

    def test_null_input(self):
        macro_output = tile_grid(None)
        assert "USAGE" in macro_output

    @pytest.mark.skip(reason="TODO")
    def test_empty_input(self):
        pass

    @pytest.mark.skip(reason="TODO")
    def test_missing_required_input(self):
        pass
