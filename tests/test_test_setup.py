import pytest
from jinja2 import TemplateNotFound

class TestTestSetup():

    def test_filesystem_terminal_loader_can_load_terminal_template(self, env_with_terminal_loader):
        try:
            found_template = env_with_terminal_loader.get_template("base.html")
            assert found_template != None
        except TemplateNotFound:
            self.fail("base.html should be found")

            