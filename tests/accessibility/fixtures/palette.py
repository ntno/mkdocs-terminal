"""Pytest fixtures for palette CSS data used by accessibility tests."""

from __future__ import annotations

import pytest

from tests.accessibility.utilities.palette_loader import (
    load_all_palette_css_attributes,
    load_palette_css_attributes,
)


@pytest.fixture
def palette_css_attributes(request):
    """Return resolved CSS attributes for a specific palette."""
    palette_name = getattr(request, "param", "default")
    return load_palette_css_attributes(palette_name)


@pytest.fixture
def all_palette_css_attributes():
    """Return resolved CSS attributes for every default palette."""
    return load_all_palette_css_attributes()
