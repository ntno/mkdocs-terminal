from jinja2 import TemplateNotFound
import pytest

class TestTestSetup():

    def test_filesystem_terminal_loader_can_load_terminal_template(self, env_with_terminal_loader):
        try:
            found_template = env_with_terminal_loader.get_template("base.html")
            assert found_template is not None
        except TemplateNotFound:
            self.fail("base.html should be found")

    @pytest.mark.parametrize("palette_css_attributes", ["default", "dark", "gruvbox_dark"], indirect=True)
    def test_palette_css_attributes_returns_dict(self, palette_css_attributes):
        """Test that palette_css_attributes returns a dictionary of CSS values."""
        assert isinstance(palette_css_attributes, dict)
        assert len(palette_css_attributes) > 0
        # Verify some expected keys are present
        expected_keys = {"font-stack", "background-color", "font-color", "primary-color"}
        assert expected_keys.issubset(palette_css_attributes.keys())


    def test_palette_css_attributes_default_palette(self, palette_css_attributes):
        """Test that default palette is used when no parameter is specified."""
        assert isinstance(palette_css_attributes, dict)
        assert len(palette_css_attributes) > 0
        # Verify some expected keys are present
        expected_keys = {"font-stack", "background-color", "font-color", "primary-color"}
        assert expected_keys.issubset(palette_css_attributes.keys())

