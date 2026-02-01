"""Tests for PalettePlugin.

Tests plugin integration with MkDocs build process, configuration
handling, and Jinja2 environment setup.
"""

import pytest
from unittest.mock import MagicMock, PropertyMock
from pathlib import Path
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
        css_content = f"/* {palette} */"
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
        assert plugin.palette_config is not None
        assert plugin.palette_config["default"] == "default"
        assert plugin.palette_config["selector_enabled"] is False
    
    def test_on_config_with_legacy_string(self, mock_mkdocs_config):
        """Test on_config with legacy string format."""
        mock_mkdocs_config.theme.get = MagicMock(return_value="dark")
        
        plugin = PalettePlugin()
        plugin.on_config(mock_mkdocs_config)
        
        assert plugin.palette_config["default"] == "dark"
        assert plugin.palette_config["selector_enabled"] is False
    
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
        
        assert plugin.palette_config["default"] == "dark"
        assert plugin.palette_config["selector_enabled"] is True
        assert plugin.palette_config["selector_ui"] == "toggle"
        assert len(plugin.palette_config["valid_options"]) == 2
    
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
        assert len(plugin.palette_config["valid_options"]) == 2
        assert plugin.palette_config["valid_options"][0]["name"] == "dark"
        assert plugin.palette_config["valid_options"][1]["name"] == "lightyear"
    
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
        
        assert len(plugin.palette_config["valid_options"]) == 2
        assert plugin.palette_config["valid_options"][0]["name"] == "ocean"


class TestOnEnv:
    """Tests for on_env event handler."""
    
    def test_on_env_adds_palette_config_to_globals(self, mock_mkdocs_config):
        """Test on_env adds palette_config to Jinja2 globals."""
        plugin = PalettePlugin()
        plugin.on_config(mock_mkdocs_config)
        
        # Create mock Jinja2 environment
        env = MagicMock()
        env.globals = {}
        
        result = plugin.on_env(env, mock_mkdocs_config, None)
        
        assert result == env
        assert "palette_config" in env.globals
        assert env.globals["palette_config"] == plugin.palette_config
    
    def test_on_env_handles_no_palette_config(self, mock_mkdocs_config):
        """Test on_env handles case when palette_config is None."""
        plugin = PalettePlugin()
        # Don't call on_config, so palette_config remains None
        
        env = MagicMock()
        env.globals = {}
        
        result = plugin.on_env(env, mock_mkdocs_config, None)
        
        assert result == env
        assert "palette_config" not in env.globals


class TestPluginIntegration:
    """Integration tests for plugin lifecycle."""
    
    def test_full_plugin_lifecycle(self, mock_mkdocs_config):
        """Test complete plugin lifecycle: init -> on_config -> on_env."""
        # Initialize plugin
        plugin = PalettePlugin()
        assert plugin.palette_config is None
        
        # Process config
        palette_config = {
            "default": "dark",
            "selector": {
                "enabled": True,
                "ui": "auto",
                "options": ["dark", "lightyear"]
            }
        }
        mock_mkdocs_config.theme.get = MagicMock(return_value=palette_config)
        plugin.on_config(mock_mkdocs_config)
        
        assert plugin.palette_config is not None
        assert plugin.palette_config["default"] == "dark"
        
        # Setup Jinja2 environment
        env = MagicMock()
        env.globals = {}
        plugin.on_env(env, mock_mkdocs_config, None)
        
        assert "palette_config" in env.globals
        assert env.globals["palette_config"]["default"] == "dark"
        assert env.globals["palette_config"]["selector_enabled"] is True
