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
        self.macro_config = None
        self.mkdocs_config = None
        self.jinja2_env = None

    def get_chatter(self):
        return self.chatter

    def get_mkdocs_config(self):
        return self.mkdocs_config

    def setup(self, env):
        self.chatter = env.start_chatting("terminal.pluglets.tile_grid")
        self.get_chatter()("set MkdocsMacroPlugin chatter: %s" % self.get_chatter())
        self.macro_config = copy(env.config)
        self.get_chatter()("macro config: %s" % self.macro_config)
        self.mkdocs_config = copy(env.conf)
        self.get_chatter()("mkdocs config: %s" % self.get_mkdocs_config())

    def define_env(self, env):
        # store macro config and setup MkdocsMacroPlugin chatter
        self.setup(env)

        # register tile_grid function with MkdocsMacroPlugin
        for fn in [tile_grid]:
            env.macro(fn)
            self.get_chatter()("added \'%s\' macro" % fn.__name__)

        # create jinja2 env for later use
        self.jinja2_env = self.create_jinja2_env(self.create_theme_file_loader(), self.create_jinja2_filters(self.get_mkdocs_config()))

    def create_jinja2_filters(self, mkdocs_config):
        """returns list of {} with name of filter and Jinja2 filter function"""
        use_markup_filter = False
        if mkdocs_config is not None and mkdocs_config.plugins is not None:
            if "terminal/md-to-html" in mkdocs_config.plugins or "md-to-html" in mkdocs_config.plugins:
                use_markup_filter = True
        filters = []
        if use_markup_filter:
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
            self.get_chatter()("added \'%s\' filter to Jinja2 Environment" % filter["name"])
            self.get_chatter()("filter: %s" % filter["function"])
        self.get_chatter()("created new Jinja2 Environment: %s" % new_jinja2_env)
        return new_jinja2_env

    def create_theme_file_loader(self):
        """returns Jinja2 FileSystemLoader initialized to the terminal theme's install directory"""
        here = Path(__file__)
        pluglet_folder = here.parent
        pluglets_folder = pluglet_folder.parent
        terminal_folder = pluglets_folder.parent
        new_theme_file_loader = loaders.FileSystemLoader(terminal_folder.resolve())
        self.get_chatter()("created new Jinja2 FileSystemLoader: %s" % new_theme_file_loader)
        return new_theme_file_loader

    def create_markup_filter(self, mkdocs_config):
        """creates new Jinja2 markup filter via MarkdownToHtmlFilterPlugin"""
        markup_plugin = MarkdownToHtmlFilterPlugin()
        markup_plugin.setup_markdown(mkdocs_config)
        self.get_chatter()("created markup filter with markdown extensions: %s" % mkdocs_config.markdown_extensions)
        self.get_chatter()("created markup filter with mdx_configs: %s" % mkdocs_config.mdx_configs)
        return markup_plugin.markupsafe_jinja2_filter
