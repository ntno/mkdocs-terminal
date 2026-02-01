"""Tests for palette configuration module.

Tests palette configuration parsing, validation, and normalization
following MkDocs configuration patterns.
"""

import pytest
from pathlib import Path
from terminal.plugins.palette.config import (
    parse_palette_config,
    validate_palette_options,
    PaletteOption,
    SelectorConfig,
    PaletteConfig
)


@pytest.fixture
def theme_dir(tmp_path):
    """Create temporary theme directory with palette CSS files."""
    palettes_dir = tmp_path / "css" / "palettes"
    palettes_dir.mkdir(parents=True)
    
    # Create bundled palette files
    for palette in ["default", "dark", "light", "blueberry", "pink"]:
        (palettes_dir / f"{palette}.css").write_text(f"/* {palette} palette */")
    
    return tmp_path


class TestConfigClasses:
    """Test MkDocs Config classes for type validation."""
    
    def test_palette_option_config(self):
        """Test PaletteOption Config class."""
        # Note: Config classes are used by MkDocs for validation
        # We're just verifying they're defined correctly
        assert hasattr(PaletteOption, 'name')
        assert hasattr(PaletteOption, 'css')
    
    def test_selector_config(self):
        """Test SelectorConfig Config class."""
        assert hasattr(SelectorConfig, 'enabled')
        assert hasattr(SelectorConfig, 'ui')
        assert hasattr(SelectorConfig, 'options')
    
    def test_palette_config(self):
        """Test PaletteConfig Config class."""
        assert hasattr(PaletteConfig, 'default')
        assert hasattr(PaletteConfig, 'selector')


class TestLegacyStringFormat:
    """Tests for legacy string format parsing."""
    
    def test_legacy_string_dark(self, theme_dir):
        """Test palette: 'dark' normalizes correctly."""
        result = parse_palette_config("dark", theme_dir)
        
        assert result["default"] == "dark"
        assert result["selector_enabled"] is False
        assert result["selector_ui"] == "auto"
        assert result["options"] == []
        assert "dark" in result["bundled_palettes"]
    
    def test_legacy_string_default(self, theme_dir):
        """Test palette: 'default' normalizes correctly."""
        result = parse_palette_config("default", theme_dir)
        
        assert result["default"] == "default"
        assert result["selector_enabled"] is False
    


class TestNewObjectFormat:
    """Tests for new object format parsing."""
    
    def test_minimal_object_config(self, theme_dir):
        """Test minimal config with only default field."""
        config_value = {"default": "dark"}
        result = parse_palette_config(config_value, theme_dir)
        
        assert result["default"] == "dark"
        assert result["selector_enabled"] is False
        assert result["selector_ui"] == "auto"
        assert result["options"] == []
    
    def test_full_object_config(self, theme_dir):
        """Test full config with all fields."""
        config_value = {
            "default": "dark",
            "selector": {
                "enabled": True,
                "ui": "select",
                "options": [
                    {"name": "dark"},
                    {"name": "light"}
                ]
            }
        }
        result = parse_palette_config(config_value, theme_dir)
        
        assert result["default"] == "dark"
        assert result["selector_enabled"] is True
        assert result["selector_ui"] == "select"
        assert len(result["options"]) == 2
        assert result["options"][0] == {"name": "dark"}
        assert result["options"][1] == {"name": "light"}
    
    def test_custom_palette_option(self, theme_dir):
        """Test config with custom palette CSS path."""
        config_value = {
            "selector": {
                "options": [
                    {"name": "ocean", "css": "assets/ocean.css"},
                    {"name": "dark"}
                ]
            }
        }
        result = parse_palette_config(config_value, theme_dir)
        
        assert len(result["options"]) == 2
        assert result["options"][0] == {"name": "ocean", "css": "assets/ocean.css"}
        assert result["options"][1] == {"name": "dark"}
    
    def test_string_options_format(self, theme_dir):
        """Test simple string format for options."""
        config_value = {
            "selector": {
                "options": ["dark", "light", "pink"]
            }
        }
        result = parse_palette_config(config_value, theme_dir)
        
        assert len(result["options"]) == 3
        assert result["options"][0] == {"name": "dark"}
        assert result["options"][1] == {"name": "light"}
        assert result["options"][2] == {"name": "pink"}


class TestDefaultValues:
    """Tests for default value application."""
    
    def test_none_config(self, theme_dir):
        """Test None config uses all defaults."""
        result = parse_palette_config(None, theme_dir)
        
        assert result["default"] == "default"
        assert result["selector_enabled"] is False
        assert result["selector_ui"] == "auto"
        assert result["options"] == []
    
    def test_empty_dict(self, theme_dir):
        """Test empty dict uses defaults."""
        result = parse_palette_config({}, theme_dir)
        
        assert result["default"] == "default"
        assert result["selector_enabled"] is False
    
    def test_missing_selector_fields(self, theme_dir):
        """Test missing selector fields use defaults."""
        config_value = {
            "selector": {}
        }
        result = parse_palette_config(config_value, theme_dir)
        
        assert result["selector_enabled"] is False
        assert result["selector_ui"] == "auto"
        assert result["options"] == []


class TestEdgeCases:
    """Tests for edge cases and invalid input."""
    
    def test_invalid_config_type(self, theme_dir):
        """Test invalid config type uses defaults."""
        result = parse_palette_config(123, theme_dir)
        
        assert result["default"] == "default"
        assert result["selector_enabled"] is False
    
    def test_invalid_selector_type(self, theme_dir):
        """Test invalid selector type uses defaults."""
        config_value = {
            "default": "dark",
            "selector": "invalid"
        }
        result = parse_palette_config(config_value, theme_dir)
        
        assert result["default"] == "dark"
        assert result["selector_enabled"] is False
    
    def test_invalid_ui_value(self, theme_dir):
        """Test invalid selector.ui value falls back to 'auto'."""
        config_value = {
            "selector": {
                "ui": "dropdown"  # Invalid
            }
        }
        result = parse_palette_config(config_value, theme_dir)
        
        assert result["selector_ui"] == "auto"
    
    def test_option_missing_name_skipped(self, theme_dir):
        """Test option without name is skipped."""
        config_value = {
            "selector": {
                "options": [
                    {"name": "dark"},
                    {"css": "missing.css"},  # No name
                    {"name": "light"}
                ]
            }
        }
        result = parse_palette_config(config_value, theme_dir)
        
        assert len(result["options"]) == 2
        assert result["options"][0]["name"] == "dark"
        assert result["options"][1]["name"] == "light"
    
    def test_invalid_option_type_skipped(self, theme_dir):
        """Test invalid option types are skipped."""
        config_value = {
            "selector": {
                "options": [
                    {"name": "dark"},
                    123,  # Invalid
                    None,  # Invalid
                    {"name": "light"}
                ]
            }
        }
        result = parse_palette_config(config_value, theme_dir)
        
        assert len(result["options"]) == 2


class TestValidation:
    """Tests for palette validation logic."""
    
    def test_validate_bundled_palettes(self, theme_dir):
        """Test validation accepts valid bundled palettes."""
        config = parse_palette_config({
            "selector": {
                "options": ["dark", "light", "blueberry"]
            }
        }, theme_dir)
        
        result = validate_palette_options(config, [])
        
        assert len(result["valid_options"]) == 3
        assert len(result["warnings"]) == 0
    
    def test_validate_invalid_bundled_palette(self, theme_dir):
        """Test validation rejects non-existent bundled palette."""
        config = parse_palette_config({
            "selector": {
                "options": ["dark", "nonexistent", "light"]
            }
        }, theme_dir)
        
        result = validate_palette_options(config, [])
        
        assert len(result["valid_options"]) == 2
        assert any("nonexistent" in w for w in result["warnings"])
    
    def test_validate_custom_palette_in_extra_css(self, theme_dir):
        """Test validation accepts custom palette in extra_css."""
        config = parse_palette_config({
            "selector": {
                "options": [
                    {"name": "ocean", "css": "assets/ocean.css"},
                    {"name": "dark"}
                ]
            }
        }, theme_dir)
        
        result = validate_palette_options(config, ["assets/ocean.css"])
        
        assert len(result["valid_options"]) == 2
        assert len(result["warnings"]) == 0
    
    def test_validate_custom_palette_missing_from_extra_css(self, theme_dir):
        """Test validation rejects custom palette not in extra_css."""
        config = parse_palette_config({
            "selector": {
                "options": [
                    {"name": "ocean", "css": "assets/ocean.css"},
                    {"name": "dark"}
                ]
            }
        }, theme_dir)
        
        result = validate_palette_options(config, [])
        
        assert len(result["valid_options"]) == 1
        assert result["valid_options"][0]["name"] == "dark"
        assert any("ocean.css" in w for w in result["warnings"])
    
    def test_validate_invalid_default_palette(self, theme_dir):
        """Test validation fixes invalid default palette."""
        config = parse_palette_config({
            "default": "nonexistent",
            "selector": {
                "options": ["dark", "light"]
            }
        }, theme_dir)
        
        result = validate_palette_options(config, [])
        
        assert result["default"] == "default"  # Falls back
        assert any("nonexistent" in w for w in result["warnings"])
    
    def test_validate_selector_disabled_when_no_valid_options(self, theme_dir):
        """Test selector disabled when all options are invalid."""
        config = parse_palette_config({
            "selector": {
                "enabled": True,
                "options": ["invalid1", "invalid2"]
            }
        }, theme_dir)
        
        result = validate_palette_options(config, [])
        
        assert result["selector_enabled"] is False
        assert len(result["valid_options"]) == 0
        assert any("Disabling selector" in w for w in result["warnings"])
    
    def test_validate_toggle_ui_requires_two_options(self, theme_dir):
        """Test toggle UI validation requires exactly 2 options."""
        config = parse_palette_config({
            "selector": {
                "enabled": True,
                "ui": "toggle",
                "options": ["dark", "light", "pink"]
            }
        }, theme_dir)
        
        result = validate_palette_options(config, [])
        
        assert result["selector_ui"] == "select"  # Falls back
        assert any("Toggle UI requires exactly 2" in w for w in result["warnings"])
    
    def test_validate_toggle_ui_with_two_options(self, theme_dir):
        """Test toggle UI accepted with exactly 2 options."""
        config = parse_palette_config({
            "selector": {
                "enabled": True,
                "ui": "toggle",
                "options": ["dark", "light"]
            }
        }, theme_dir)
        
        result = validate_palette_options(config, [])
        
        assert result["selector_ui"] == "toggle"
        assert len(result["warnings"]) == 0


class TestBundledPalettesDetection:
    """Tests for detecting available bundled palettes."""
    
    def test_detects_bundled_palettes(self, theme_dir):
        """Test detection of palette CSS files."""
        result = parse_palette_config(None, theme_dir)
        
        bundled = result["bundled_palettes"]
        assert "default" in bundled
        assert "dark" in bundled
        assert "light" in bundled
        assert "blueberry" in bundled
        assert "pink" in bundled
        assert len(bundled) == 5
    
    def test_handles_missing_palettes_directory(self, tmp_path):
        """Test graceful handling when palettes directory doesn't exist."""
        result = parse_palette_config(None, tmp_path)
        
        assert result["bundled_palettes"] == []
