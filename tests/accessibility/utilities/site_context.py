"""Site context helpers shared by accessibility tests."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterator, List, Optional, Set, Union

from bs4 import BeautifulSoup

from .css_parser import extract_css_variables

PathLike = Union[str, Path]


@dataclass
class SiteContext:
    """Context for a built MkDocs HTML file with parsed CSS data.

    Args:
        site_path: Root directory containing the built MkDocs site.
        html_file: Absolute path to the HTML file represented by this context.
        html_content: Raw HTML contents of ``html_file``.
        css_content: Combined CSS text loaded for the page.
        css_variables: Mapping of CSS custom properties extracted from the page.
        soup: BeautifulSoup instance for ``html_content``.
    """

    site_path: Path
    html_file: Path
    html_content: str
    css_content: str
    css_variables: Dict[str, str]
    soup: BeautifulSoup


class SiteContextBuilder:
    """Build and cache :class:`SiteContext` objects for a built site.

    Args:
        site_path: Path to the built MkDocs site (absolute or relative).
    """

    def __init__(self, site_path: PathLike):
        self.site_path = ensure_site_path(site_path)
        self._html_files: Optional[List[Path]] = None
        self._html_cache: Dict[Path, str] = {}
        self._css_cache: Dict[Path, str] = {}
        self._css_variable_cache: Dict[Path, Dict[str, str]] = {}
        self._soup_cache: Dict[Path, BeautifulSoup] = {}

    def iter_html_files(self) -> Iterator[SiteContext]:
        """Yield :class:`SiteContext` objects for every HTML file in the site.

        Args:
            None.

        Returns:
            Iterator of contexts ordered by relative path. Example return: the
            first yielded item typically has ``relative_path == "index.html"``.
        """
        for html_file in self._get_html_files():
            yield self.build_context(html_file)

    def build_context(self, html_file: PathLike) -> SiteContext:
        """Build a :class:`SiteContext` for ``html_file`` and cache the result.

        Args:
            html_file: Absolute path or path relative to the built site root.

        Returns:
            A fully populated :class:`SiteContext`. Example return: a context
            whose ``relative_path`` is ``"docs/install/index.html"``.
        """
        html_path = resolve_html_file(self.site_path, html_file)
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
            self._css_variable_cache[html_file] = extract_css_variables(html_content, css_content)
        return self._css_variable_cache[html_file]

    def _get_soup(self, html_file: Path, html_content: str) -> BeautifulSoup:
        if html_file not in self._soup_cache:
            self._soup_cache[html_file] = BeautifulSoup(html_content, "html.parser")
        return self._soup_cache[html_file]


def load_css_from_site(site_path: Path, html_content: str) -> str:
    """Load concatenated CSS referenced by ``html_content`` within ``site_path``.

    Args:
        site_path: Root of the built site being inspected.
        html_content: HTML string that may reference CSS files.

    Returns:
        Combined CSS text for the page. Example return: ``"body { color:#111; }\n"``.
    """
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

            css_path = resolve_css_path(site_path, css_file)
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
    """Yield :class:`SiteContext` objects for every HTML file under ``site_path``.

    Args:
        site_path: Path-like reference to the built site root.

    Returns:
        Iterator of :class:`SiteContext` objects. Example return: yields a
        context whose ``relative_path`` is ``"index.html"``.
    """
    builder = SiteContextBuilder(site_path)
    yield from builder.iter_html_files()


def get_site_path(site_path: PathLike) -> Path:
    """Validate and return a :class:`Path` to the built site.

    Args:
        site_path: Path-like reference to the built site root.

    Returns:
        Absolute :class:`Path` to the site. Example return:
        ``Path("/tmp/mkdocs/site")``.
    """
    return ensure_site_path(site_path)


def ensure_site_path(site_path: PathLike) -> Path:
    """Ensure ``site_path`` exists and contains at least one HTML file.

    Args:
        site_path: Path-like reference to validate.

    Returns:
        Absolute :class:`Path` pointing to the site directory. Example return:
        ``Path("/workspace/tests/site")``.

    Raises:
        AssertionError: If the directory is missing or lacks HTML files.
    """
    path = Path(site_path).resolve()
    if not path.exists():
        raise AssertionError(f"Built site not found at {path}")
    html_files = list(path.glob("**/*.html"))
    if not html_files:
        raise AssertionError(f"No HTML files found in {path}")
    return path


def resolve_html_file(site_path: Path, html_file: PathLike) -> Path:
    """Resolve an HTML file path relative to ``site_path``.

    Args:
        site_path: Root directory containing the built site.
        html_file: Absolute path or path relative to ``site_path``.

    Returns:
        Absolute :class:`Path` to the HTML file. Example return:
        ``Path("/tmp/site/docs/index.html")``.

    Raises:
        FileNotFoundError: If the resolved file does not exist.
    """
    html_path = Path(html_file)
    if not html_path.is_absolute():
        html_path = site_path / html_path
    html_path = html_path.resolve()
    if not html_path.exists():
        raise FileNotFoundError(f"HTML file not found: {html_path}")
    return html_path


def resolve_css_path(site_path: Path, css_reference: str) -> Path:
    """Resolve a CSS ``href`` reference to a path under ``site_path``.

    Args:
        site_path: Root directory containing the built site.
        css_reference: Value from a ``<link rel="stylesheet">`` ``href`` attribute.

    Returns:
        Absolute :class:`Path` to the CSS file. Example return:
        ``Path("/tmp/site/css/terminal.css")``.
    """
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
