from terminal.pluglets.tile_grid.util import grid


class TestTileGridPluglet():

    def test_null_input(self):
        macro_output = grid(None)
        assert macro_output == "invalid_tiles"
