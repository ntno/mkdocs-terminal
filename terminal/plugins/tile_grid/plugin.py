from jinja2.utils import markupsafe
import logging
import markdown
from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin
from mkdocs.commands.build import DuplicateFilter
from .tile_grid import TileGrid
# mkdocs.exceptions.PluginError

DEFAULT_TILE_MARKER = "boop"
DEFAULT_MARKUP_FILTER_NAME = "markup"
DEFAULT_GRID_PARTIAL_PATH = "partials/tile-grid/tiles.html"

class TileGridPlugin(BasePlugin):

    config_scheme = (
        ('marker', config_options.Type(str, default=DEFAULT_TILE_MARKER)),
    )

    def __init__(self):
        self.md = None
        self.grid_partial = None
        self.env = None

    def setup_markdown(self, config):
        self.md = markdown.Markdown(
            extensions=config.markdown_extensions or [],
            extension_configs=config.mdx_configs or {}
        )
        
    def on_pre_build(self, config):
        logger.info("TileGridPlugin::on_pre_build::markdown_extensions: %s", config.markdown_extensions)
        logger.info("TileGridPlugin::on_pre_build::mdx_configs': %s", config.mdx_configs)
        self.setup_markdown(config)
        logger.info("TileGridPlugin::on_pre_build::md: %s", self.md)
        return

    def markupsafe_jinja2_filter(self, text, **kwargs):
        return markupsafe.Markup(self.md.convert(text))

    def on_env(self, env, config, files, **kwargs):
        env.filters[DEFAULT_MARKUP_FILTER_NAME] = self.markupsafe_jinja2_filter
        logger.warning("TileGridPlugin::on_env::%s: %s", DEFAULT_MARKUP_FILTER_NAME, self.markupsafe_jinja2_filter)
        self.grid_partial = env.get_template(DEFAULT_GRID_PARTIAL_PATH)
        logger.warning("TileGridPlugin::on_env::grid_partial: %s", self.grid_partial)
        self.env = env
        return env





    def on_page_markdown(self, markdown, page, config, files, **kwargs):
        if DEFAULT_TILE_MARKER in markdown:
            return "its in there "
        else:
            return "couldnt find that marker"
        # if DEFAULT_TILE_MARKER in markdown and self.grid_partial and "tiles" in page.meta and len(page.meta["tiles"]) > 0:
        #     logger.warning("TileGridPlugin::on_page_markdown::tiles:%s", len(page.meta["tiles"]))
        #     context_data = {
        #         "page": {
        #             "meta": {
        #                 "tiles": page.meta["tiles"]
        #             }
        #         }
        #     }
        #     logger.warning("TileGridPlugin::on_env::context_data: %s", context_data)
        #     rendered_grid = self.grid_partial.render(context_data)
        #     logger.warning("TileGridPlugin::on_env::rendered_grid: %s", rendered_grid)
        #     markdown = markdown.replace(DEFAULT_TILE_MARKER, rendered_grid)
        #     # markdown = re.sub(r"\{\{(\s)*dolly(\s)*\}\}",
        #     #                   random_lyrics(),
        #     #                   markdown,
        #     #                   flags=re.IGNORECASE)
        #     return markdown
        
        # return markdown

    # def on_page_content(self, html, page, config, files, **kwargs):
    #     logger.warning("on_page_content")
    #     return html

    # def on_page_context(self, context, page, config, nav, **kwargs):
    #     logger.warning("on_page_context")
    #     return context

    # def on_post_page(self, output_content, page, config, **kwargs):
    #     logger.warning("on_post_page")
    #     return output_content


# -----------------------------------------------------------------------------
# Data
# -----------------------------------------------------------------------------

# Set up logging
logger = logging.getLogger("mkdocs")
logger.addFilter(DuplicateFilter())