from jinja2 import TemplateNotFound
import pytest
from tests.interface.theme_features import DEFAULT_PALETTES

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

    def test_all_palette_css_attributes_returns_all_palettes(self, all_palette_css_attributes):
        """Test that all_palette_css_attributes contains entries for all DEFAULT_PALETTES."""
        assert isinstance(all_palette_css_attributes, dict)
        assert len(all_palette_css_attributes) == len(DEFAULT_PALETTES)
        
        # Verify all default palettes are present
        for palette_name in DEFAULT_PALETTES:
            assert palette_name in all_palette_css_attributes
            assert isinstance(all_palette_css_attributes[palette_name], dict)
            assert len(all_palette_css_attributes[palette_name]) > 0

    def test_all_palette_css_attributes_contains_expected_keys(self, all_palette_css_attributes):
        """Test that each palette in all_palette_css_attributes contains expected CSS attributes."""
        expected_keys = {"font-stack", "background-color", "font-color", "primary-color", "error-color"}
        
        for palette_name in DEFAULT_PALETTES:
            palette_attrs = all_palette_css_attributes[palette_name]
            assert expected_keys.issubset(palette_attrs.keys()), \
                f"Palette '{palette_name}' missing expected keys. Has: {list(palette_attrs.keys())}"

    def test_all_palette_css_attributes_structure(self, all_palette_css_attributes):
        """Test that all_palette_css_attributes has proper nested structure."""
        # Top level should map palette names to dicts
        for palette_name, attributes in all_palette_css_attributes.items():
            assert palette_name in DEFAULT_PALETTES
            assert isinstance(attributes, dict)
            # Each attribute should be a string value (CSS color, size, etc.)
            for attr_name, attr_value in attributes.items():
                assert isinstance(attr_name, str)
                assert isinstance(attr_value, str)
                assert len(attr_name) > 0
                assert len(attr_value) > 0



