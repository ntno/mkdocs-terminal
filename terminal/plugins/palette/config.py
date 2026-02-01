"""Palette configuration for mkdocs-terminal theme.

This module provides configuration handling for theme palette options,
following MkDocs configuration patterns similar to mkdocs-material plugins.

Configuration format:
    Legacy (string):
        theme:
          palette: "dark"

    New (object):
        theme:
          palette:
            default: "dark"
            selector:
              enabled: true
              ui: "auto"  # or "toggle", "select"
              options:
                - name: "dark"
                - name: "light"
                - name: "custom"
                  css: "assets/custom.css"
"""

import logging
from pathlib import Path
from typing import Any, Dict, List

from mkdocs.config.base import Config
from mkdocs.config.config_options import ListOfItems, Optional as OptionalType, Type

# -----------------------------------------------------------------------------
# Classes
# -----------------------------------------------------------------------------


class PaletteOption(Config):
    """Configuration for a single palette option.

    Attributes:
        name: Palette identifier (required)
        css: Optional custom CSS file path for non-bundled palettes
    """
    name = Type(str)
    css = OptionalType(Type(str))


class SelectorConfig(Config):
    """Configuration for palette selector UI.

    Attributes:
        enabled: Whether to show selector UI
        ui: Control type ("auto", "toggle", or "select")
        options: List of available palette options
    """
    enabled = Type(bool, default=False)
    ui = Type(str, default="auto")
    options = ListOfItems(Type((str, dict)), default=[])


class PaletteConfig(Config):
    """Main palette configuration for mkdocs-terminal theme.

    Supports both legacy string format and new object format.

    Attributes:
        default: Default palette name
        selector: Selector configuration (when using object format)
    """
    default = Type(str, default="default")
    selector = OptionalType(Type(dict))


# -----------------------------------------------------------------------------
# Functions
# -----------------------------------------------------------------------------

def parse_palette_config(config_value: Any, theme_dir: Path) -> Dict[str, Any]:
    """Parse and normalize palette configuration.

    Handles both legacy string format and new object format, validates
    palette names and CSS paths, and returns normalized configuration
    for use in templates.

    Args:
        config_value: Raw palette config from mkdocs.yml theme section
        theme_dir: Path to theme directory for validating bundled palettes

    Returns:
        Normalized palette configuration dict with keys:
            - default: str
            - selector_enabled: bool
            - selector_ui: str
            - options: List[Dict[str, str]]
            - bundled_palettes: List[str] (available bundled palette names)
    """
    # Get list of bundled palettes
    palettes_dir = theme_dir / "css" / "palettes"
    bundled_palettes = []
    if palettes_dir.exists():
        bundled_palettes = [
            p.stem for p in palettes_dir.glob("*.css")
        ]

    # Handle None or missing config
    if config_value is None:
        return {
            "default": "default",
            "selector_enabled": False,
            "selector_ui": "auto",
            "options": [],
            "bundled_palettes": bundled_palettes
        }

    # Handle legacy string format: palette: "dark"
    if isinstance(config_value, str):
        return {
            "default": config_value,
            "selector_enabled": False,
            "selector_ui": "auto",
            "options": [],
            "bundled_palettes": bundled_palettes
        }

    # Handle new object format
    if not isinstance(config_value, dict):
        log.warning(
            f"Invalid palette config type: {type(config_value).__name__}. "
            "Expected string or dict. Using defaults."
        )
        return {
            "default": "default",
            "selector_enabled": False,
            "selector_ui": "auto",
            "options": [],
            "bundled_palettes": bundled_palettes
        }

    # Extract values
    default_palette = config_value.get("default", "default")
    selector_config = config_value.get("selector", {})

    if not isinstance(selector_config, dict):
        log.warning(
            f"Invalid selector config type: {type(selector_config).__name__}. "
            "Expected dict. Using defaults."
        )
        selector_config = {}

    selector_enabled = selector_config.get("enabled", False)
    selector_ui = selector_config.get("ui", "auto")

    # Validate selector UI value
    valid_ui_types = ["auto", "toggle", "select"]
    if selector_ui not in valid_ui_types:
        log.warning(
            f"Invalid selector.ui value '{selector_ui}'. "
            f"Must be one of: {', '.join(valid_ui_types)}. Using 'auto'."
        )
        selector_ui = "auto"

    # Parse palette options
    options_raw = selector_config.get("options", [])
    options = []

    for opt in options_raw:
        if isinstance(opt, str):
            # Simple string option
            options.append({"name": opt})
        elif isinstance(opt, dict):
            # Object option with name and optional css
            name = opt.get("name")
            css = opt.get("css")
            
            # If no name but CSS provided, derive name from CSS filename
            if not name and css:
                # Extract basename without extension (e.g., "assets/ocean.css" -> "ocean")
                name = Path(css).stem
                log.debug(f"Auto-derived palette name '{name}' from CSS path '{css}'")
            
            if name:
                opt_dict = {"name": name}
                if css:
                    opt_dict["css"] = css
                options.append(opt_dict)
            else:
                log.warning(f"Palette option missing 'name' field and 'css' field, skipping: {opt}")
        else:
            log.warning(
                f"Invalid palette option type: {type(opt).__name__}, skipping: {opt}"
            )

    return {
        "default": default_palette,
        "selector_enabled": selector_enabled,
        "selector_ui": selector_ui,
        "options": options,
        "bundled_palettes": bundled_palettes
    }


def validate_palette_options(
    palette_config: Dict[str, Any],
    extra_css: List[str]
) -> Dict[str, Any]:
    """Validate palette options and filter invalid entries.

    Checks that:
    - Bundled palette names exist in theme's palettes directory
    - Custom palette CSS paths are listed in extra_css
    - At least one valid option exists if selector is enabled

    Args:
        palette_config: Normalized palette config from parse_palette_config
        extra_css: List of extra CSS files from MkDocs config

    Returns:
        Updated palette config with:
            - Invalid options removed from options list
            - valid_options: List[Dict] of validated options
            - warnings: List[str] of validation warnings
    """
    bundled_palettes = palette_config["bundled_palettes"]
    options = palette_config["options"]
    valid_options = []
    warnings = []

    for opt in options:
        name = opt["name"]
        css = opt.get("css")

        if css:
            # Custom palette - check if CSS path is in extra_css
            if css not in extra_css:
                warnings.append(
                    f"Custom palette '{name}' CSS file '{css}' not found in extra_css. "
                    f"Add to mkdocs.yml: extra_css: ['{css}']"
                )
                continue
        else:
            # Bundled palette - check if it exists
            if name not in bundled_palettes:
                warnings.append(
                    f"Bundled palette '{name}' not found. "
                    f"Available palettes: {', '.join(bundled_palettes)}"
                )
                continue

        valid_options.append(opt)

    # Validate default palette
    default_name = palette_config["default"]
    default_in_options = any(opt["name"] == default_name for opt in valid_options)
    default_is_bundled = default_name in bundled_palettes

    if not default_is_bundled and not default_in_options:
        warnings.append(
            f"Default palette '{default_name}' is not a valid bundled palette "
            f"and not in selector options. Using 'default'."
        )
        palette_config["default"] = "default"

    # Check selector has valid options
    if palette_config["selector_enabled"]:
        if not valid_options:
            warnings.append(
                "Selector enabled but no valid palette options found. "
                "Disabling selector."
            )
            palette_config["selector_enabled"] = False
        elif palette_config["selector_ui"] == "toggle" and len(valid_options) != 2:
            warnings.append(
                f"Toggle UI requires exactly 2 options, found {len(valid_options)}. "
                f"Using 'select' UI instead."
            )
            palette_config["selector_ui"] = "select"

    # Log all warnings
    for warning in warnings:
        log.warning(warning)

    palette_config["valid_options"] = valid_options
    palette_config["warnings"] = warnings

    return palette_config


# -----------------------------------------------------------------------------
# Data
# -----------------------------------------------------------------------------

# Set up logging
log = logging.getLogger("mkdocs.terminal.palette")
