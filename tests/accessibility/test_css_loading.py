"""Debug test to check CSS loading in built sites."""

import pytest
from pathlib import Path
from bs4 import BeautifulSoup
from tests.interface.theme_features import DEFAULT_PALETTES


class TestCSSLoading:
    """Debug tests for CSS file loading."""

    @pytest.mark.parametrize("built_example_site_with_palette", [
        ("minimal", palette) for palette in DEFAULT_PALETTES
    ], indirect=True)
    def test_check_css_in_built_site(self, built_example_site_with_palette):
        """Check what CSS files are actually included in the built HTML."""

        site_path = Path(built_example_site_with_palette)
        html_file = site_path / 'index.html'

        with open(html_file) as f:
            html_content = f.read()

        # Parse HTML to find CSS links
        soup = BeautifulSoup(html_content, 'html.parser')
        head = soup.find('head')

        if not head:
            pytest.fail("No head element found in HTML")

        # Find all <link> tags with rel='stylesheet'
        link_tags = head.find_all('link', rel='stylesheet')
        css_links = [link.get('href') for link in link_tags if link.get('href', '').endswith('.css')]

        print(f"\n\nCSS files in built site {site_path.name}:")
        for link in css_links:
            print(f"  {link}")

        # Check for palette CSS
        palette_file = None
        for link in css_links:
            if 'css/palettes/' in link:
                palette_file = link
                break

        assert palette_file is not None, f"No palette CSS found in {css_links}"
        print(f"\nPalette CSS: {palette_file}")
