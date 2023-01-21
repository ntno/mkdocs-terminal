from jinja2.environment import Environment
from terminal.pluglets.tile_grid.util import tile_grid
from terminal.plugins.md_to_html.plugin import MarkdownToHtmlFilterPlugin, DEFAULT_MARKUP_FILTER_NAME
from jinja2 import loaders
from pathlib import Path
from copy import copy


class TileGridMacroEnvironment(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(TileGridMacroEnvironment, cls).__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        self.chatter = None
        self.conf = None
        self.config = None
        self.jinja2_env = None

    def setup(self, env):
        # store runtime info from MkdocsMacroPlugin
        self.conf = copy(env.conf)
        self.config = copy(env.config)

        # setup MkdocsMacroPlugin logger
        self.chatter = env.start_chatting("terminal.pluglets.tile_grid")

    def define_env(self, env):
        # store runtime info and setup chatter
        self.setup(env)

        # register grid function with MkdocsMacroPlugin
        for fn in [tile_grid]:
            env.macro(fn)
            self.chatter("added %s macro" % fn.__name__)

        # create jinja2 env for later use

        self.jinja2_env = self.create_jinja2_env(self.create_theme_file_loader(), self.create_jinja2_filters(self.conf))

    def create_jinja2_filters(self, mkdocs_config):
        """returns list of {} with name of filter and Jinja2 filter function"""
        filters = []
        filters.append({
            "name": DEFAULT_MARKUP_FILTER_NAME,
            "function": self.create_markup_filter(mkdocs_config)
        })
        return filters

    def create_jinja2_env(self, loader, filters):
        """returns Jinja2 Environment with given loader and filters"""
        new_jinja2_env = Environment()
        new_jinja2_env.loader = loader
        for filter in filters:
            new_jinja2_env.filters[filter["name"]] = filter["function"]
        self.chatter("created new Jinja2 Environment: %s" % new_jinja2_env)
        return new_jinja2_env

    def create_theme_file_loader(self):
        """returns Jinja2 FileSystemLoader initialized to the terminal theme's install directory"""
        here = Path(__file__)
        pluglet_folder = here.parent
        pluglets_folder = pluglet_folder.parent
        terminal_folder = pluglets_folder.parent
        new_theme_file_loader = loaders.FileSystemLoader(terminal_folder.resolve())
        self.chatter("created new Jinja2 FileSystemLoader: %s" % new_theme_file_loader)
        return new_theme_file_loader

    def create_markup_filter(self, mkdocs_config):
        """creates new Jinja2 markup filter via MarkdownToHtmlFilterPlugin"""
        markup_plugin = MarkdownToHtmlFilterPlugin()
        markup_plugin.setup_markdown(mkdocs_config)
        self.chatter("created markup filter with markdown extensions %s" % mkdocs_config["markdown_extensions"])
        self.chatter("created markup filter with mdx_configs %s" % mkdocs_config["mdx_configs"])
        return markup_plugin.markupsafe_jinja2_filter