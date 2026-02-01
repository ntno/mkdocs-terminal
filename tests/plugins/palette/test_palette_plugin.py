"""Tests for PalettePlugin.

Tests plugin integration with MkDocs build process, configuration
handling, and Jinja2 environment setup.
"""

import pytest
from unittest.mock import MagicMock
from terminal.plugins.palette.plugin import PalettePlugin


@pytest.fixture
def mock_mkdocs_config(tmp_path):
    """Create mock MkDocs config."""
    # Create theme directory structure
    theme_dir = tmp_path / "theme"
    palettes_dir = theme_dir / "css" / "palettes"
    palettes_dir.mkdir(parents=True)

    # Create palette files
    for palette in ["default", "dark", "lightyear"]:
        palette_file = palettes_dir / f"{palette}.css"
        css_content = f"/* Test {palette} Palette */"
        palette_file.write_text(css_content)

    config = MagicMock()
    config.theme.dirs = [str(theme_dir)]
    config.theme.get = MagicMock(return_value=None)
    config.extra_css = []

    return config


class TestPalettePluginInitialization:
    """Tests for plugin initialization."""

    def test_plugin_initialization(self):
        """Test plugin initializes with None palette_config."""
        plugin = PalettePlugin()
        assert plugin.palette_config is None


class TestOnConfig:
    """Tests for on_config event handler."""

    def test_on_config_with_no_palette_config(self, mock_mkdocs_config):
        """Test on_config with no palette configuration."""
        plugin = PalettePlugin()
        result = plugin.on_config(mock_mkdocs_config)

        assert result == mock_mkdocs_config
        assert mock_mkdocs_config.theme.palette_config is not None
        assert mock_mkdocs_config.theme.palette_config["default"] == "default"
        assert mock_mkdocs_config.theme.palette_config["selector_enabled"] is False

    def test_on_config_with_legacy_string(self, mock_mkdocs_config):
        """Test on_config with legacy string format."""
        mock_mkdocs_config.theme.get = MagicMock(return_value="dark")

        plugin = PalettePlugin()
        plugin.on_config(mock_mkdocs_config)

        assert mock_mkdocs_config.theme.palette_config["default"] == "dark"
        assert mock_mkdocs_config.theme.palette_config["selector_enabled"] is False

    def test_on_config_with_new_format(self, mock_mkdocs_config):
        """Test on_config with new object format."""
        palette_config = {
            "default": "dark",
            "selector": {
                "enabled": True,
                "ui": "toggle",
                "options": [
                    {"name": "dark"},
                    {"name": "lightyear"}
                ]
            }
        }
        mock_mkdocs_config.theme.get = MagicMock(return_value=palette_config)

        plugin = PalettePlugin()
        plugin.on_config(mock_mkdocs_config)

        assert mock_mkdocs_config.theme.palette_config["default"] == "dark"
        assert mock_mkdocs_config.theme.palette_config["selector_enabled"] is True
        assert mock_mkdocs_config.theme.palette_config["selector_ui"] == "toggle"
        assert len(mock_mkdocs_config.theme.palette_config["valid_options"]) == 2

    def test_on_config_validates_options(self, mock_mkdocs_config):
        """Test on_config validates palette options."""
        palette_config = {
            "selector": {
                "enabled": True,
                "options": [
                    {"name": "dark"},
                    {"name": "invalid"},  # Should be filtered
                    {"name": "lightyear"}
                ]
            }
        }
        mock_mkdocs_config.theme.get = MagicMock(return_value=palette_config)

        plugin = PalettePlugin()
        plugin.on_config(mock_mkdocs_config)

        # Invalid palette should be filtered out
        assert len(mock_mkdocs_config.theme.palette_config["valid_options"]) == 2
        assert mock_mkdocs_config.theme.palette_config["valid_options"][0]["name"] == "dark"
        assert mock_mkdocs_config.theme.palette_config["valid_options"][1]["name"] == "lightyear"

    def test_on_config_with_custom_palette(self, mock_mkdocs_config):
        """Test on_config with custom palette in extra_css."""
        palette_config = {
            "selector": {
                "options": [
                    {"name": "ocean", "css": "assets/ocean.css"},
                    {"name": "dark"}
                ]
            }
        }
        mock_mkdocs_config.theme.get = MagicMock(return_value=palette_config)
        mock_mkdocs_config.extra_css = ["assets/ocean.css"]

        plugin = PalettePlugin()
        plugin.on_config(mock_mkdocs_config)

        assert len(mock_mkdocs_config.theme.palette_config["valid_options"]) == 2
        assert mock_mkdocs_config.theme.palette_config["valid_options"][0]["name"] == "ocean"
