# helpers copied from mkdocs/mkdocs
# https://github.com/mkdocs/mkdocs/blob/master/mkdocs/tests/base.py

from __future__ import annotations
from mkdocs.config.defaults import MkDocsConfig
import os


def load_config(config_file_path: str | None = None, **cfg) -> MkDocsConfig:
    """Helper to build a simple config for testing."""
    path_base = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'integration', 'base')
    if 'site_name' not in cfg:
        cfg['site_name'] = 'Example'
    if 'docs_dir' not in cfg:
        # Point to an actual dir to avoid a 'does not exist' error on validation.
        cfg['docs_dir'] = os.path.join(path_base, 'docs')
    if 'plugins' not in cfg:
        cfg['plugins'] = []
    conf = MkDocsConfig(config_file_path=config_file_path or os.path.join(path_base, 'mkdocs.yml'))
    conf.load_dict(cfg)

    errors_warnings = conf.validate()
    assert errors_warnings == ([], []), errors_warnings
    return conf
