# Copyright (c) 2018 Byrne Reese
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# import os
# import sys
# import re
# from timeit import default_timer as timer
# from datetime import datetime, timedelta
# from mkdocs import utils as mkdocs_utils
# from mkdocs.config import config_options, Config
# from mkdocs.plugins import BasePlugin
import jinja2
# from jinja2.ext import Extension
from jinja2.utils import markupsafe
import logging
import markdown
# from timeit import default_timer as timer
# from datetime import datetime, timedelta
# from mkdocs import utils as mkdocs_utils
from mkdocs.config import config_options
# from mkdocs.config import Config
from mkdocs.plugins import BasePlugin
from mkdocs.commands.build import DuplicateFilter

class MarkdownToHtmlFilterPlugin(BasePlugin):

    config_scheme = (
        ('param', config_options.Type(str, default='')),
    )

    def __init__(self):
        self.enabled = True
        self.total_time = 0
        self.md = None

    def setup_markdown(self, config):
        logger.warning("setting markdown_extensions: %s", config.markdown_extensions)
        logger.warning("setting mdx_configs': %s", config.mdx_configs)
        self.md = markdown.Markdown(
            extensions=config.markdown_extensions or [],
            extension_configs=config.mdx_configs or {}
        )

    def on_pre_build(self, config):
        logger.warning("on_pre_build")
        self.setup_markdown(config)
        return

    def markdown_jinja2_filter(self, text, **kwargs):
        logger.warning("markdown_jinja2_filter")
        return markupsafe.Markup(self.md.convert(text))

    def on_env(self, env, config, files, **kwargs):
        logger.warning("on_env")
        self.config = config
        env.filters['markdown'] = self.markdown_jinja2_filter
        grid_partial = env.get_template("partials/tile-grid/tiles.html")
        yolo = grid_partial.render("")
        # context_data = {
        #         "page": {
        #             "meta": {
        #                 "tiles": page.meta["tiles"]
        #             }
        #         }
        #     }

        # logger.warning("loaders: ", env.loaders)
        return env

    # def on_serve(self, server, **kwargs):
    #     logger.warning("on_serve")
    #     return server

    # def on_files(self, files, config, **kwargs):
    #     logger.warning("on_files")
    #     return files

    # def on_nav(self, nav, config, files, **kwargs):
    #     logger.warning("on_nav")
    #     return nav

    # def on_config(self, config, **kwargs):
    #     logger.warning("on_config")
    #     return config

    # def on_post_build(self, config, **kwargs):
    #     logger.warning("on_post_build")
    #     return

    # def on_pre_page(self, page, config, files, **kwargs):
    #     logger.warning("on_pre_page")
    #     return page

    # def on_page_read_source(self, page, config, **kwargs):
    #     logger.warning("on_page_read_source")
    #     return ""

    def on_page_markdown(self, markdown, page, config, files, **kwargs):
        logger.warning("on_page_markdown")
        logger.warning("page.meta %s", page.meta)
        if "tiles" in page.meta:
            for tile in page.meta["tiles"]:
                if "caption" in tile:
                    logger.warning("tile.caption: %s", tile["caption"])
                    tile["caption"] = markupsafe.Markup(self.md.convert(tile["caption"]))
                    logger.warning("(now) tile.caption: %s", tile["caption"])
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