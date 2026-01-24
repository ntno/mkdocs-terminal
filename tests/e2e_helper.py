"""Utilities for building example MkDocs sites for tests."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import yaml
from mkdocs.commands.build import build
from tests.integration_helper import load_config


def build_example_site(
    tmp_path_factory,
    example_name: str = "minimal",
    palette_name: Optional[str] = None,
):
    """Build the requested example site with an optional palette override."""
    suffix = f"_{palette_name}" if palette_name else ""
    tmp_dir = tmp_path_factory.mktemp(f"built_{example_name}{suffix}_site")

    tests_dir = Path(__file__).parent
    example_dir = tests_dir / "examples" / example_name
    docs_dir = example_dir / "docs"
    theme_dir = tests_dir.parent / "terminal"

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
    }
    if palette_name is not None:
        theme_config["palette"] = palette_name

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
