"""Tests for palette application mechanism in styles.html partial.

Tests verify that:
- FOUC prevention script is rendered
- Correct palette CSS files are linked based on configuration
- data-available-palettes is properly embedded
- Selector enabled/disabled modes work correctly
"""

from tests.utils.html import assert_valid_html
import pytest
import json


@pytest.fixture
def styles_partial(env_with_terminal_loader):
    """Load the styles.html partial template."""
    return env_with_terminal_loader.get_template("partials/styles.html")


@pytest.fixture
def base_context():
    """Minimal context for rendering styles partial."""
    return {
        "config": {
            "theme": {
                "palette": "default",
                "palette_config": {},
                "features": []
            }
        }
    }


class TestFOUCPreventionScript:
    """Test inline FOUC prevention script rendering."""

    def test_fouc_script_present_in_output(self, styles_partial, base_context):
        """FOUC prevention script should be present in rendered output."""
        rendered = styles_partial.render(base_context)
        assert "localStorage.getItem('mkdocs-terminal-palette')" in rendered
        assert_valid_html(rendered)

    def test_fouc_script_validates_against_available_palettes(self, styles_partial, base_context):
        """FOUC script should validate saved palette against available options."""
        base_context["config"]["theme"]["palette_config"] = {
            "selector_enabled": True,
            "valid_options": [
                {"name": "dark", "label": "Dark"},
                {"name": "light", "label": "Light"}
            ]
        }
        rendered = styles_partial.render(base_context)
        assert "available.indexOf(saved)" in rendered
        assert '["dark","light"]' in rendered or '["dark", "light"]' in rendered
        assert_valid_html(rendered)

    def test_fouc_script_handles_empty_options(self, styles_partial, base_context):
        """FOUC script should handle empty valid_options gracefully."""
        base_context["config"]["theme"]["palette_config"] = {
            "selector_enabled": False,
            "valid_options": []
        }
        rendered = styles_partial.render(base_context)
        assert "[]" in rendered
        assert_valid_html(rendered)

    def test_fouc_script_appears_before_css_links(self, styles_partial, base_context):
        """FOUC script must appear before CSS links to prevent flash."""
        rendered = styles_partial.render(base_context)
        script_pos = rendered.find("<script>")
        css_pos = rendered.find('<link href="')
        assert script_pos > 0, "Script should be present"
        assert css_pos > 0, "CSS links should be present"
        assert script_pos < css_pos, "Script must appear before CSS links"


class TestSelectorDisabled:
    """Test palette CSS linking when selector is disabled."""

    def test_only_default_palette_linked_when_selector_disabled(self, styles_partial, base_context):
        """When selector disabled, only default palette should be linked."""
        base_context["config"]["theme"]["palette"] = "dark"
        base_context["config"]["theme"]["palette_config"] = {
            "selector_enabled": False,
            "valid_options": []
        }
        rendered = styles_partial.render(base_context)
        
        # Should include dark palette
        assert 'css/palettes/dark.css' in rendered
        
        # Should not include other palettes
        assert 'css/palettes/light.css' not in rendered
        assert 'css/palettes/gruvbox_dark.css' not in rendered
        assert_valid_html(rendered)

    def test_default_palette_used_when_none_specified(self, styles_partial, base_context):
        """When no palette specified, default.css should be linked."""
        base_context["config"]["theme"]["palette_config"] = {
            "selector_enabled": False,
            "valid_options": []
        }
        rendered = styles_partial.render(base_context)
        assert 'css/palettes/default.css' in rendered
        assert_valid_html(rendered)


class TestSelectorEnabled:
    """Test palette CSS linking when selector is enabled."""

    def test_all_valid_options_linked_when_selector_enabled(self, styles_partial, base_context):
        """When selector enabled, all valid option palettes should be linked."""
        base_context["config"]["theme"]["palette_config"] = {
            "selector_enabled": True,
            "valid_options": [
                {"name": "dark", "label": "Dark"},
                {"name": "light", "label": "Light"},
                {"name": "gruvbox_dark", "label": "Gruvbox Dark"}
            ]
        }
        rendered = styles_partial.render(base_context)
        
        # All configured palettes should be linked
        assert 'css/palettes/dark.css' in rendered
        assert 'css/palettes/light.css' in rendered
        assert 'css/palettes/gruvbox_dark.css' in rendered
        
        # Comment annotations should be present
        assert 'Bundled palette: dark' in rendered
        assert 'Bundled palette: light' in rendered
        assert 'Bundled palette: gruvbox_dark' in rendered
        
        assert_valid_html(rendered)

    def test_custom_palette_css_path_used(self, styles_partial, base_context):
        """When custom palette specified, custom CSS path should be used."""
        base_context["config"]["theme"]["palette_config"] = {
            "selector_enabled": True,
            "valid_options": [
                {"name": "dark", "label": "Dark"},
                {"name": "custom", "label": "Custom", "css": "css/custom-palette.css"}
            ]
        }
        rendered = styles_partial.render(base_context)
        
        # Bundled palette should use standard path
        assert 'css/palettes/dark.css' in rendered
        assert 'Bundled palette: dark' in rendered
        
        # Custom palette should use custom path
        assert 'css/custom-palette.css' in rendered
        assert 'Custom palette: custom' in rendered
        
        assert_valid_html(rendered)

    def test_mixed_bundled_and_custom_palettes(self, styles_partial, base_context):
        """Selector should handle mix of bundled and custom palettes."""
        base_context["config"]["theme"]["palette_config"] = {
            "selector_enabled": True,
            "valid_options": [
                {"name": "dark", "label": "Dark"},
                {"name": "custom1", "label": "Custom 1", "css": "css/custom1.css"},
                {"name": "light", "label": "Light"},
                {"name": "custom2", "label": "Custom 2", "css": "css/custom2.css"}
            ]
        }
        rendered = styles_partial.render(base_context)
        
        # Bundled palettes
        assert 'css/palettes/dark.css' in rendered
        assert 'css/palettes/light.css' in rendered
        
        # Custom palettes
        assert 'css/custom1.css' in rendered
        assert 'css/custom2.css' in rendered
        
        assert_valid_html(rendered)


class TestSelectorEnabledButNoValidOptions:
    """Test edge case: selector enabled but no valid options."""

    def test_falls_back_to_default_when_no_valid_options(self, styles_partial, base_context):
        """When selector enabled but no valid options, should fall back to default."""
        base_context["config"]["theme"]["palette"] = "dark"
        base_context["config"]["theme"]["palette_config"] = {
            "selector_enabled": True,
            "valid_options": []  # No valid options
        }
        rendered = styles_partial.render(base_context)
        
        # Should fall back to linking default palette
        assert 'css/palettes/dark.css' in rendered
        assert_valid_html(rendered)


class TestHTMLStructure:
    """Test overall HTML structure and ordering."""

    def test_core_css_files_always_linked(self, styles_partial, base_context):
        """Core CSS files should always be linked regardless of palette config."""
        rendered = styles_partial.render(base_context)
        
        # Core CSS files
        assert 'css/fontawesome/css/fontawesome.min.css' in rendered
        assert 'css/fontawesome/css/solid.min.css' in rendered
        assert 'css/normalize.css' in rendered
        assert 'css/terminal.css' in rendered
        assert 'css/theme.css' in rendered
        assert 'css/theme.tile_grid.css' in rendered
        assert 'css/theme.footer.css' in rendered
        
        assert_valid_html(rendered)

    def test_css_load_order_correct(self, styles_partial, base_context):
        """CSS files should load in correct order: core → palettes."""
        rendered = styles_partial.render(base_context)
        
        terminal_css_pos = rendered.find('css/terminal.css')
        theme_css_pos = rendered.find('css/theme.css')
        palette_css_pos = rendered.find('css/palettes/')
        
        assert terminal_css_pos < theme_css_pos, "terminal.css before theme.css"
        assert theme_css_pos < palette_css_pos, "theme.css before palettes"

    def test_inline_styles_present(self, styles_partial, base_context):
        """Inline styles for layout should be present."""
        rendered = styles_partial.render(base_context)
        assert '.terminal-mkdocs-main-grid' in rendered
        assert 'grid-template-columns' in rendered
        assert_valid_html(rendered)


class TestPaletteComments:
    """Test HTML comments documenting palette configuration."""

    def test_bundled_palette_comments(self, styles_partial, base_context):
        """Bundled palettes should have descriptive comments."""
        base_context["config"]["theme"]["palette_config"] = {
            "selector_enabled": True,
            "valid_options": [
                {"name": "dark", "label": "Dark"}
            ]
        }
        rendered = styles_partial.render(base_context)
        assert 'Bundled palette: dark' in rendered

    def test_custom_palette_comments(self, styles_partial, base_context):
        """Custom palettes should have descriptive comments."""
        base_context["config"]["theme"]["palette_config"] = {
            "selector_enabled": True,
            "valid_options": [
                {"name": "ocean", "label": "Ocean", "css": "css/ocean.css"}
            ]
        }
        rendered = styles_partial.render(base_context)
        assert 'Custom palette: ocean' in rendered

    def test_selector_state_comments(self, styles_partial, base_context):
        """Output should include comments about selector state."""
        base_context["config"]["theme"]["palette_config"] = {
            "selector_enabled": True,
            "valid_options": [{"name": "dark", "label": "Dark"}]
        }
        rendered_enabled = styles_partial.render(base_context)
        assert 'Palette selector enabled' in rendered_enabled
        
        base_context["config"]["theme"]["palette_config"]["selector_enabled"] = False
        rendered_disabled = styles_partial.render(base_context)
        assert 'Palette selector disabled' in rendered_disabled
