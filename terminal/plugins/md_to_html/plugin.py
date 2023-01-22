from mkdocs.plugins import BasePlugin
from mkdocs.commands.build import DuplicateFilter
from jinja2.utils import markupsafe
import markdown
import logging
DEFAULT_MARKUP_FILTER_NAME = "markup"


class MarkdownToHtmlFilterPlugin(BasePlugin):

    def __init__(self):
        self.md = None

    def setup_markdown(self, config):
        self.md = markdown.Markdown(
            extensions=config.markdown_extensions or [],
            extension_configs=config.mdx_configs or {}
        )

    def on_pre_build(self, config, **kwargs):
        logger.debug("MarkdownToHtmlFilterPlugin::on_pre_build::markdown_extensions: %s", config.markdown_extensions)
        logger.debug("MarkdownToHtmlFilterPlugin::on_pre_build::mdx_configs': %s", config.mdx_configs)
        self.setup_markdown(config)
        logger.debug("MarkdownToHtmlFilterPlugin::on_pre_build::md: %s", self.md)
        return

    def markupsafe_jinja2_filter(self, text, **kwargs):
        return markupsafe.Markup(self.md.convert(text))

    def on_env(self, env, config, files, **kwargs):
        env.filters[DEFAULT_MARKUP_FILTER_NAME] = self.markupsafe_jinja2_filter
        logger.debug("MarkdownToHtmlFilterPlugin::on_env::%s: %s", DEFAULT_MARKUP_FILTER_NAME, self.markupsafe_jinja2_filter)
        self.env = env
        return env


# Set up logging
logger = logging.getLogger("mkdocs.terminal.md_to_html")
logger.addFilter(DuplicateFilter())
