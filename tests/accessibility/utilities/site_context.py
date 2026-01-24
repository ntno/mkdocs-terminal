"""Site context helpers shared by accessibility tests."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterator, List, Optional, Set, Union

from bs4 import BeautifulSoup

from .css_parser import _extract_css_variables

PathLike = Union[str, Path]


@dataclass
class SiteContext:
    """Context for a built MkDocs HTML file with parsed CSS data."""

    site_path: Path
    html_file: Path
    html_content: str
    css_content: str
    css_variables: Dict[str, str]
    soup: BeautifulSoup

    @property
    def relative_path(self) -> str:
        """Return the file path relative to the built site root."""
        return str(self.html_file.relative_to(self.site_path))


class SiteContextBuilder:
    """Builds and caches :class:`SiteContext` objects for a built site."""

    def __init__(self, site_path: PathLike):
        self.site_path = _ensure_site_path(site_path)
        self._html_files: Optional[List[Path]] = None
        self._html_cache: Dict[Path, str] = {}
        self._css_cache: Dict[Path, str] = {}
        self._css_variable_cache: Dict[Path, Dict[str, str]] = {}
        self._soup_cache: Dict[Path, BeautifulSoup] = {}

    def iter_html_files(self) -> Iterator[SiteContext]:
        """Yield :class:`SiteContext` for every HTML file in the site."""
        for html_file in self._get_html_files():
            yield self.build_context(html_file)

    def build_context(self, html_file: PathLike) -> SiteContext:
        """Build a :class:`SiteContext` for ``html_file`` (cached when possible)."""
        html_path = _resolve_html_file(self.site_path, html_file)
        html_content = self._get_html_content(html_path)
        css_content = self._get_css_content(html_path, html_content)
        css_variables = self._get_css_variables(html_path, html_content, css_content)
        soup = self._get_soup(html_path, html_content)

        return SiteContext(
            site_path=self.site_path,
            html_file=html_path,
            html_content=html_content,
            css_content=css_content,
            css_variables=css_variables,
            soup=soup,
        )

    def _get_html_files(self) -> List[Path]:
        if self._html_files is None:
            self._html_files = sorted(self.site_path.glob("**/*.html"))
            if not self._html_files:
                raise AssertionError(f"No HTML files found in {self.site_path}")
        return self._html_files

    def _get_html_content(self, html_file: Path) -> str:
        if html_file not in self._html_cache:
            self._html_cache[html_file] = html_file.read_text(encoding="utf-8")
        return self._html_cache[html_file]

    def _get_css_content(self, html_file: Path, html_content: str) -> str:
        if html_file not in self._css_cache:
            self._css_cache[html_file] = load_css_from_site(self.site_path, html_content)
        return self._css_cache[html_file]

    def _get_css_variables(self, html_file: Path, html_content: str, css_content: str) -> Dict[str, str]:
        if html_file not in self._css_variable_cache:
            self._css_variable_cache[html_file] = _extract_css_variables(html_content, css_content)
        return self._css_variable_cache[html_file]

    def _get_soup(self, html_file: Path, html_content: str) -> BeautifulSoup:
        if html_file not in self._soup_cache:
            self._soup_cache[html_file] = BeautifulSoup(html_content, "html.parser")
        return self._soup_cache[html_file]


def load_css_from_site(site_path: Path, html_content: str) -> str:
    """Load concatenated CSS referenced by ``html_content`` within ``site_path``."""
    css_content = ""
    loaded_paths: Set[Path] = set()
    active_palette = None

    soup = BeautifulSoup(html_content, "html.parser")
    head = soup.find("head")

    if head:
        for link in head.find_all("link", rel="stylesheet"):
            href = link.get("href")
            if not href or not href.endswith(".css"):
                continue

            css_file = href.split("?")[0]
            palette_match = re.match(r".*/css/palettes/([^/]+)\.css$", css_file)
            if palette_match:
                active_palette = palette_match.group(1)

            css_path = _resolve_css_path(site_path, css_file)
            if not css_path.exists():
                continue

            resolved = css_path.resolve()
            if resolved in loaded_paths:
                continue

            try:
                css_content += css_path.read_text(encoding="utf-8") + "\n"
                loaded_paths.add(resolved)
            except OSError:
                continue

    if active_palette:
        palette_css_path = site_path / "css" / "palettes" / f"{active_palette}.css"
        resolved_palette = palette_css_path.resolve()
        if palette_css_path.exists() and resolved_palette not in loaded_paths:
            try:
                css_content += palette_css_path.read_text(encoding="utf-8") + "\n"
            except OSError:
                pass

    return css_content


def iter_site_html_files(site_path: PathLike) -> Iterator[SiteContext]:
    """Yield :class:`SiteContext` objects for every HTML file under ``site_path``."""
    builder = SiteContextBuilder(site_path)
    yield from builder.iter_html_files()


def get_site_path(site_path: PathLike) -> Path:
    """Validate and return a :class:`Path` to the built site."""
    return _ensure_site_path(site_path)


def _ensure_site_path(site_path: PathLike) -> Path:
    path = Path(site_path).resolve()
    if not path.exists():
        raise AssertionError(f"Built site not found at {path}")
    html_files = list(path.glob("**/*.html"))
    if not html_files:
        raise AssertionError(f"No HTML files found in {path}")
    return path


def _resolve_html_file(site_path: Path, html_file: PathLike) -> Path:
    html_path = Path(html_file)
    if not html_path.is_absolute():
        html_path = site_path / html_path
    html_path = html_path.resolve()
    if not html_path.exists():
        raise FileNotFoundError(f"HTML file not found: {html_path}")
    return html_path


def _resolve_css_path(site_path: Path, css_reference: str) -> Path:
    """Resolve a CSS ``href`` reference to a path under ``site_path``."""
    css_path = Path(css_reference)
    if css_path.is_absolute():
        relative_css = css_path.relative_to("/")
        return (site_path / relative_css).resolve()
    return (site_path / css_path).resolve()


__all__ = [
    "SiteContext",
    "SiteContextBuilder",
    "get_site_path",
    "iter_site_html_files",
    "load_css_from_site",
]
