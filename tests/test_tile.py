import pytest
from tests.tile import Tile

class TestTile():
    def test_empty_tile(self):
        t = Tile()
        self.assertFalse(t.is_valid)
        self.assertFalse(t.is_link_only)
        self.assertFalse(t.is_img_only)
        self.assertFalse(t.is_linked_img)

    def test_minimal_link_tile(self):
        t = Tile(link_href="https://example.com")
        self.assertTrue(t.is_valid)
        self.assertTrue(t.is_link_only)
        self.assertFalse(t.is_img_only)
        self.assertFalse(t.is_linked_img)

    def test_minimal_img_tile(self):
        t = Tile(img_src="https://github.githubassets.com/favicons/favicon.svg")
        self.assertTrue(t.is_valid)
        self.assertFalse(t.is_link_only)
        self.assertTrue(t.is_img_only)
        self.assertFalse(t.is_linked_img)

    def test_minimal_linked_image(self):
        t = Tile(link_href="https://github.com", img_src="https://github.githubassets.com/favicons/favicon.svg")
        self.assertTrue(t.is_valid)
        self.assertFalse(t.is_link_only)
        self.assertFalse(t.is_img_only)
        self.assertTrue(t.is_linked_img)

