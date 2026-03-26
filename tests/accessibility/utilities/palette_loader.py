"""Helpers for loading palette CSS attributes for accessibility tests."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Dict

from tests.accessibility.utilities import load_palette_context
from tests.interface.theme_features import DEFAULT_PALETTES

PROJECT_ROOT = Path(__file__).resolve().parents[3]
PALETTES_DIR = PROJECT_ROOT / "terminal" / "css" / "palettes"
FALLBACK_CSS_PATH = PROJECT_ROOT / "terminal" / "css" / "terminal.css"


def validate_palette_name(palette_name: str) -> str:
    """Normalize and validate palette names against ``DEFAULT_PALETTES``.

    Args:
        palette_name: Palette identifier such as ``"default"`` or ``"sans_dark"``.

    Returns:
        Sanitized palette name guaranteed to exist in ``DEFAULT_PALETTES``.
        Example return: passing ``" default "`` yields ``"default"``.

    Raises:
        ValueError: If the palette does not exist in ``DEFAULT_PALETTES``.
    """

    name = palette_name.strip()
    if name not in DEFAULT_PALETTES:
        raise ValueError(
            f"Palette '{palette_name}' not found in DEFAULT_PALETTES. Valid palettes: {DEFAULT_PALETTES}"
        )
    return name


@lru_cache(maxsize=None)
def read_text_file(path: Path) -> str:
    """Read UTF-8 text from ``path`` while caching the result.

    Args:
        path: Absolute path pointing to a CSS file.

    Returns:
        Contents of the file as a string. Example return: ``"body { color: #fff; }"``.

    Raises:
        FileNotFoundError: If ``path`` does not exist.
    """

    if not path.exists():
        raise FileNotFoundError(f"CSS file not found: {path}")
    return path.read_text(encoding="utf-8")


@lru_cache(maxsize=1)
def get_fallback_css() -> str:
    """Return cached contents of the fallback ``terminal.css`` file.

    Args:
        None.

    Returns:
        Fallback CSS text used when palette-specific attributes are missing.
        Example return: ``"body { --font-color: #e6edf3; }"``.
    """

    return read_text_file(FALLBACK_CSS_PATH)


def load_palette_css_attributes(palette_name: str) -> Dict[str, str]:
    """Return resolved CSS attributes for a single palette with full cascade.

    This function loads the complete CSS cascade (terminal.css → theme.css →
    palette file) and resolves variables through the [data-palette] architecture.

    Args:
        palette_name: Name of the palette to load (e.g., "dark", "gruvbox_dark").

    Returns:
        Dictionary of resolved attributes such as ``{"background-color": "#0d1117"}``.
        Example return: ``{"background-color": "#0d1117", "font-color": "#e6edf3"}``.

    Raises:
        ValueError: If palette_name is not in DEFAULT_PALETTES.
        FileNotFoundError: If required CSS files don't exist.
    """
    name = validate_palette_name(palette_name)
    return load_palette_context(name)


def load_all_palette_css_attributes() -> Dict[str, Dict[str, str]]:
    """Return resolved CSS attributes for every palette in ``DEFAULT_PALETTES``.

    Loads the complete CSS cascade for each palette using the [data-palette]
    architecture.

    Args:
        None.

    Returns:
        Dictionary keyed by palette name whose values mirror the structure
        returned by :func:`load_palette_css_attributes`. Example return:
        ``{"default": {"font-color": "#111"}, "sans": {"font-color": "#333"}}``.
    """
    all_attributes: Dict[str, Dict[str, str]] = {}
    for palette_name in DEFAULT_PALETTES:
        all_attributes[palette_name] = load_palette_context(palette_name)
    return all_attributes
