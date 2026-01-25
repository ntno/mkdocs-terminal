"""Utility helpers shared across accessibility tests."""

from .css_parser import (
    extract_css_attributes,
    extract_css_variables,
    get_element_computed_styles,
    parse_css_variables,
    resolve_css_variable,
)
from .palette_loader import load_all_palette_css_attributes, load_palette_css_attributes
from .site_context import (
    SiteContext,
    SiteContextBuilder,
    get_site_path,
    iter_site_html_files,
    load_css_from_site,
)

__all__ = [
    "extract_css_attributes",
    "extract_css_variables",
    "get_element_computed_styles",
    "parse_css_variables",
    "resolve_css_variable",
    "load_palette_css_attributes",
    "load_all_palette_css_attributes",
    "SiteContext",
    "SiteContextBuilder",
    "get_site_path",
    "iter_site_html_files",
    "load_css_from_site",
]
