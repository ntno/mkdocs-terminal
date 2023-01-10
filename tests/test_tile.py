import pytest
from tests.tile import Tile

class TestTile():

    def test_empty_tile(self):
        t = Tile()
        assert t.is_valid == False
        assert t.is_link_only == False
        assert t.is_img_only == False 
        assert t.is_linked_img == False 

    def test_minimal_link_tile(self):
        t = Tile(link_href="https://example.com")
        assert t.is_valid == True
        assert t.is_link_only == True
        assert t.is_img_only == False
        assert t.is_linked_img == False 

    def test_minimal_img_tile(self):
        t = Tile(img_src="https://github.githubassets.com/favicons/favicon.svg")
        assert t.is_valid == True
        assert t.is_link_only == False
        assert t.is_img_only == True
        assert t.is_linked_img == False

    def test_minimal_linked_image(self):
        t = Tile(link_href="https://github.com", img_src="https://github.githubassets.com/favicons/favicon.svg")
        assert t.is_valid == True
        assert t.is_link_only == False
        assert t.is_img_only == False
        assert t.is_linked_img == True

