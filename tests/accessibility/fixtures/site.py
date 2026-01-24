"""Site-building fixtures dedicated to accessibility tests."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml
from mkdocs.commands.build import build
from tests.integration_helper import load_config


@pytest.fixture(scope="session")
def built_example_site_with_palette(tmp_path_factory, request):
    """Build an example site with a specified palette for accessibility tests."""
    example_name, palette_name = getattr(request, "param", ("minimal", "default"))

    tmp_dir = tmp_path_factory.mktemp(f"built_{example_name}_{palette_name}_site")
    example_dir = Path(__file__).resolve().parents[2] / "examples" / example_name
    docs_dir = example_dir / "docs"
    theme_dir = Path(__file__).resolve().parents[3] / "terminal"

    if not docs_dir.exists():
        raise ValueError(f"Example site not found at {docs_dir}")

    mkdocs_yml = example_dir / "mkdocs.yml"
    site_name = "Test Site"
    plugins = None
    markdown_extensions = None
    if mkdocs_yml.exists():
        with mkdocs_yml.open(encoding="utf-8") as f:
            config_data = yaml.safe_load(f)
            if config_data:
                site_name = config_data.get("site_name", site_name)
                plugins = config_data.get("plugins", plugins)
                markdown_extensions = config_data.get("markdown_extensions", markdown_extensions)

    theme_config = {
        "name": None,
        "custom_dir": str(theme_dir.resolve()),
        "palette": palette_name,
    }

    config_kwargs = dict(
        docs_dir=str(docs_dir.resolve()),
        site_dir=str(tmp_dir.resolve()),
        site_name=site_name,
        theme=theme_config,
    )
    if plugins is not None:
        config_kwargs["plugins"] = plugins
    if markdown_extensions is not None:
        config_kwargs["markdown_extensions"] = markdown_extensions

    config = load_config(**config_kwargs)
    build(config)
    return tmp_dir
