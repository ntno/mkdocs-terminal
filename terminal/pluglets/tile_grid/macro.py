from jinja2.environment import Environment
from terminal.pluglets.tile_grid.util import grid
from terminal.plugins.md_to_html.plugin import MarkdownToHtmlFilterPlugin, DEFAULT_MARKUP_FILTER_NAME
from jinja2 import loaders
from pathlib import Path
from copy import copy

class TileGridMkDocsMacro():
    def __init__(self) -> None:
        self.chatter = None
        self.conf = None
        self.config = None
        self.markup_plugin = MarkdownToHtmlFilterPlugin()
        self.jinja2_env = None

    def define_env(self, env):
        "Setup Jinja2 environment for TileGridMkDocsMacro based on info from MkdocsMacroPlugin"
        self.conf = copy(env.conf)
        self.config = copy(env.config)

        self.chatter = env.start_chatting("terminal.pluglets.tile_grid")
        self.markup_plugin.setup_markdown(self.conf)

        # register markup filter for macro environment
        env.filter(self.markup_plugin.markupsafe_jinja2_filter, DEFAULT_MARKUP_FILTER_NAME)
        self.chatter("added %s filter", DEFAULT_MARKUP_FILTER_NAME)

        # register grid function
        for fn in [grid]:
            env.macro(fn)
            self.chatter("added %s macro" % fn.__name__)

        # set jinja2 env for later use by macro
        self.jinja2_env = self.createJinja2Env()
        
    def createJinja2Env(self):
        new_jinja2_env = Environment()
        new_jinja2_env.loader = self.theme_file_loader()
        new_jinja2_env.filters[DEFAULT_MARKUP_FILTER_NAME] = self.markup_plugin.markupsafe_jinja2_filter
        self.chatter("creating new jinja2 environment: %s", new_jinja2_env)
        return new_jinja2_env

    def theme_file_loader(self):
        """returns Jinja2 FileSystemLoader initialized to the terminal theme's install directory"""
        here = Path(__file__)
        print("macro.py: ", here)
        pluglet_folder = here.parent
        print("pluglet_folder: ", pluglet_folder)
        pluglets_folder = pluglet_folder.parent
        print("pluglets_folder: ", pluglets_folder)
        terminal_folder = pluglets_folder.parent
        print("terminal folder: ", terminal_folder)
        return loaders.FileSystemLoader(terminal_folder.resolve())

