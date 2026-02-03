"""Tests for data attributes on HTML element in base.html template.

Tests verify that:
- data-palette attribute is set correctly
- data-available-palettes attribute contains correct JSON
- Attributes work with various palette configurations
"""

from tests.utils.html import assert_valid_html
import pytest
import json
import re


@pytest.fixture
def base_template(env_with_terminal_loader):
    """Load the base.html template."""
    return env_with_terminal_loader.get_template("base.html")


@pytest.fixture
def minimal_context():
    """Minimal context for rendering base template."""
    return {
        "config": {
            "site_name": "Test Site",
            "site_description": "Test Description",
            "theme": {
                "palette": "default",
                "palette_config": {},
                "features": []
            },
            "plugins": []
        },
        "page": {
            "title": "Test Page",
            "content": "<p>Test content</p>",
            "meta": {},
            "toc": []
        },
        "nav": []
    }


class TestDataPaletteAttribute:
    """Test data-palette attribute on <html> element."""

    def test_data_palette_attribute_present(self, base_template, minimal_context):
        """data-palette attribute should be present on html element."""
        rendered = base_template.render(minimal_context)
        assert 'data-palette="default"' in rendered
        assert_valid_html(rendered)

    @pytest.mark.parametrize("palette_name", [
        "dark",
        "light", 
        "gruvbox_dark",
        "sans",
        "sans_dark",
        "pink",
        "blueberry",
        "lightyear",
        "red_drum"
    ])
    def test_data_palette_reflects_configured_palette(self, base_template, minimal_context, palette_name):
        """data-palette should match the configured palette name."""
        minimal_context["config"]["theme"]["palette"] = palette_name
        rendered = base_template.render(minimal_context)
        expected_attr = f'data-palette="{palette_name}"'
        assert expected_attr in rendered
        assert_valid_html(rendered)

    def test_data_palette_defaults_to_default(self, base_template, minimal_context):
        """When no palette configured, data-palette should be 'default'."""
        minimal_context["config"]["theme"]["palette"] = None
        rendered = base_template.render(minimal_context)
        assert 'data-palette="default"' in rendered
        assert_valid_html(rendered)


class TestDataAvailablePalettesAttribute:
    """Test data-available-palettes attribute on <html> element."""

    def test_data_available_palettes_attribute_present(self, base_template, minimal_context):
        """data-available-palettes attribute should be present."""
        rendered = base_template.render(minimal_context)
        assert 'data-available-palettes=' in rendered
        assert_valid_html(rendered)

    def test_empty_when_no_valid_options(self, base_template, minimal_context):
        """When no valid options, data-available-palettes should be empty string."""
        minimal_context["config"]["theme"]["palette_config"] = {
            "valid_options": []
        }
        rendered = base_template.render(minimal_context)
        
        # Extract the attribute value
        match = re.search(r'data-available-palettes="([^"]*)"', rendered)
        assert match, "data-available-palettes attribute should be present"
        
        # Should be empty string
        attr_value = match.group(1)
        assert attr_value == ""
        assert_valid_html(rendered)

    def test_contains_valid_option_names(self, base_template, minimal_context):
        """data-available-palettes should contain names of valid options as comma-separated string."""
        minimal_context["config"]["theme"]["palette_config"] = {
            "valid_options": [
                {"name": "dark", "label": "Dark"},
                {"name": "light", "label": "Light"},
                {"name": "custom", "label": "Custom", "css": "css/custom.css"}
            ]
        }
        rendered = base_template.render(minimal_context)
        
        # Extract and parse the attribute
        match = re.search(r'data-available-palettes="([^"]*)"', rendered)
        assert match
        attr_value = match.group(1)
        palettes = attr_value.split(',') if attr_value else []
        
        assert len(palettes) == 3
        assert "dark" in palettes
        assert "light" in palettes
        assert "custom" in palettes
        assert_valid_html(rendered)

    def test_only_names_not_full_objects(self, base_template, minimal_context):
        """data-available-palettes should contain only names as comma-separated string."""
        minimal_context["config"]["theme"]["palette_config"] = {
            "valid_options": [
                {"name": "dark", "label": "Dark Theme", "css": None},
                {"name": "light", "label": "Light Theme", "css": None}
            ]
        }
        rendered = base_template.render(minimal_context)
        
        match = re.search(r'data-available-palettes="([^"]*)"', rendered)
        attr_value = match.group(1)
        palettes = attr_value.split(',') if attr_value else []
        
        # Should be simple list of strings, not objects
        assert isinstance(palettes, list)
        assert all(isinstance(p, str) for p in palettes)
        assert palettes == ["dark", "light"]
        assert_valid_html(rendered)

    def test_handles_missing_palette_config(self, base_template, minimal_context):
        """Should handle missing palette_config gracefully."""
        minimal_context["config"]["theme"].pop("palette_config", None)
        rendered = base_template.render(minimal_context)
        
        # Should still render with empty string
        match = re.search(r'data-available-palettes="([^"]*)"', rendered)
        assert match
        attr_value = match.group(1)
        assert attr_value == ""
        assert_valid_html(rendered)


class TestAttributeInteraction:
    """Test interaction between data-palette and data-available-palettes."""

    def test_default_palette_not_required_in_available(self, base_template, minimal_context):
        """Default palette doesn't need to be in available palettes list."""
        minimal_context["config"]["theme"]["palette"] = "dark"
        minimal_context["config"]["theme"]["palette_config"] = {
            "valid_options": [
                {"name": "light", "label": "Light"}
            ]
        }
        rendered = base_template.render(minimal_context)
        
        # data-palette should be "dark"
        assert 'data-palette="dark"' in rendered
        
        # But available should only contain "light"
        match = re.search(r'data-available-palettes="([^"]*)"', rendered)
        attr_value = match.group(1).replace('&quot;', '"')
        if attr_value:
            palettes = attr_value.split(',')
        else:
            palettes = []
        assert_valid_html(rendered)

    def test_default_palette_can_be_in_available(self, base_template, minimal_context):
        """Default palette can also be in available palettes list."""
        minimal_context["config"]["theme"]["palette"] = "dark"
        minimal_context["config"]["theme"]["palette_config"] = {
            "valid_options": [
                {"name": "dark", "label": "Dark"},
                {"name": "light", "label": "Light"}
            ]
        }
        rendered = base_template.render(minimal_context)
        
        assert 'data-palette="dark"' in rendered
        
        match = re.search(r'data-available-palettes="([^"]*)"', rendered)
        attr_value = match.group(1).replace('&quot;', '"')
        if attr_value:
            palettes = attr_value.split(',')
        else:
            palettes = []
        assert "light" in palettes
        assert_valid_html(rendered)


class TestHTMLElementStructure:
    """Test overall <html> element structure."""

    def test_html_element_has_lang_attribute(self, base_template, minimal_context):
        """HTML element should have lang attribute."""
        rendered = base_template.render(minimal_context)
        assert '<html' in rendered
        assert 'lang="en"' in rendered
        assert_valid_html(rendered)

    def test_both_attributes_on_same_element(self, base_template, minimal_context):
        """Both data attributes should be on the html element."""
        minimal_context["config"]["theme"]["palette_config"] = {
            "valid_options": [{"name": "dark", "label": "Dark"}]
        }
        rendered = base_template.render(minimal_context)
        
        # Find the <html> opening tag
        html_tag_match = re.search(r'<html[^>]+>', rendered)
        assert html_tag_match, "Should find opening html tag"
        
        html_tag = html_tag_match.group(0)
        assert 'data-palette=' in html_tag
        assert 'data-available-palettes=' in html_tag
        assert 'lang=' in html_tag
        assert_valid_html(rendered)
