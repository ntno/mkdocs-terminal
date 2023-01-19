from jinja2.utils import markupsafe
import logging
import markdown
from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin
from mkdocs.commands.build import DuplicateFilter
from .tile_grid import TileGrid
# mkdocs.exceptions.PluginError

DEFAULT_TILE_MARKER = "{{tiles}}"
DEFAULT_MARKUP_FILTER_NAME = "markup"
DEFAULT_GRID_PARTIAL_PATH = "partials/tile-grid/tiles.html"

class TileGridPlugin(BasePlugin):

    config_scheme = (
        ('marker', config_options.Type(str, default=DEFAULT_TILE_MARKER)),
    )

    def __init__(self):
        self.md = None
        self.grid_partial = None

    def setup_markdown(self, config):
        logger.debug("TileGridPlugin::setting markdown_extensions: %s", config.markdown_extensions)
        logger.debug("TileGridPlugin::setting mdx_configs': %s", config.mdx_configs)
        self.md = markdown.Markdown(
            extensions=config.markdown_extensions or [],
            extension_configs=config.mdx_configs or {}
        )

    def on_pre_build(self, config):
        self.setup_markdown(config)
        return

    def markupsafe_jinja2_filter(self, text, **kwargs):
        return markupsafe.Markup(self.md.convert(text))

    def on_env(self, env, config, files, **kwargs):
        env.filters[DEFAULT_MARKUP_FILTER_NAME] = self.markupsafe_jinja2_filter
        self.grid_partial = env.get_template(DEFAULT_GRID_PARTIAL_PATH)
        return env

    def on_page_markdown(self, markdown, page, config, files, **kwargs):
        if self.grid_partial is not None:
            if "tiles" in page.meta and len(page.meta["tiles"]) > 0:
                context_data = {
                    "page": {
                        "meta": {
                            "tiles": page.meta["tiles"]
                        }
                    }
                }
                rendered_grid = self.grid_partial.render(context_data)
                markdown = markdown.replace(DEFAULT_TILE_MARKER, rendered_grid)
                # markdown = re.sub(r"\{\{(\s)*dolly(\s)*\}\}",
                #                   random_lyrics(),
                #                   markdown,
                #                   flags=re.IGNORECASE)
                return markdown
        else:
            logger.warning("grid_partial is None, skipping for now")
        return markdown

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