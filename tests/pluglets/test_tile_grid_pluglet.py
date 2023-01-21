from terminal.pluglets.tile_grid.util import tile_grid


class TestTileGridPluglet():

    def test_null_input(self):
        macro_output = tile_grid(None)
        assert "USAGE" in macro_output
