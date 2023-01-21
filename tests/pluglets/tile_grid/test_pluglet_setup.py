import pytest


@pytest.mark.skip(reason="TODO")
class TestTileGridPlugletSetup():

    def test_that_markup_filter_not_added_when_plugin_disabled(self):
        pass

    @pytest.mark.parametrize("plugin_name", [
        pytest.param(
            "md-to-html", id="implicit-theme-namespace"
        ),
        pytest.param(
            "terminal/md-to-html", id="explicit-theme-namespace"
        )
    ])
    def test_that_markup_filter_added_when_plugin_enabled(self, plugin_name):
        assert "md-to-html" in plugin_name
        pass
