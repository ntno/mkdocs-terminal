"""Site-building fixtures dedicated to accessibility tests."""

from __future__ import annotations

import pytest

from tests.e2e_helper import build_example_site


@pytest.fixture(scope="session")
def built_example_site_with_palette(tmp_path_factory, request):
    """Build an example site with a specified palette for accessibility tests."""
    example_name, palette_name = getattr(request, "param", ("minimal", "default"))
    return build_example_site(tmp_path_factory, example_name, palette_name)
