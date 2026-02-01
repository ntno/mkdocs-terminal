"""Palette plugin for mkdocs-terminal theme.

This plugin processes palette configuration from mkdocs.yml, validates
palette options, and makes normalized configuration available to theme
templates via the Jinja2 environment.
"""

import logging
from pathlib import Path
from mkdocs.plugins import BasePlugin
from mkdocs.commands.build import DuplicateFilter

from .config import parse_palette_config, validate_palette_options


class PalettePlugin(BasePlugin):
    """Plugin to handle palette configuration for mkdocs-terminal theme.

    This plugin:
    - Parses palette configuration (legacy string or new object format)
    - Validates bundled palette names against available CSS files
    - Validates custom palette CSS paths are in extra_css
    - Makes normalized palette config available to templates
    """

    def __init__(self):
        super().__init__()
        self.palette_config = None

    def on_config(self, config, **kwargs):
        """Process palette configuration during MkDocs build.

        Args:
            config: MkDocs configuration object

        Returns:
            Modified config with palette_config added to theme
        """
        # Get theme directory path
        theme_dirs = config.theme.dirs
        theme_dir = Path(theme_dirs[0]) if theme_dirs else Path(__file__).parent.parent.parent

        # Get palette config from theme settings
        palette_value = config.theme.get("palette")

        # Parse palette configuration
        logger.debug("Parsing palette config: %s", palette_value)
        palette_config = parse_palette_config(palette_value, theme_dir)
        logger.debug("Parsed palette config: %s", palette_config)

        # Validate palette options
        extra_css = config.extra_css or []
        palette_config = validate_palette_options(palette_config, extra_css)

        # Log validation results
        if palette_config.get("warnings"):
            for warning in palette_config["warnings"]:
                logger.warning(warning)

        logger.info(
            "Palette config: default='%s', selector=%s, valid_options=%d",
            palette_config["default"],
            palette_config["selector_enabled"],
            len(palette_config.get("valid_options", []))
        )

        # Store for use in templates
        #self.palette_config = palette_config
        config.theme.palette_config = palette_config
        config.theme.palette = palette_config["default"]
        return config


# Set up logging
logger = logging.getLogger("mkdocs.terminal.palette")
logger.addFilter(DuplicateFilter())
