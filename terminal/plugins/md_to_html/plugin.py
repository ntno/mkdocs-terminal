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
from mkdocs.plugins import BasePlugin
import jinja2
# from jinja2.ext import Extension
import markdown


class MarkdownToHtmlFilterPlugin(BasePlugin):

    config_scheme = (
    )

    def __init__(self):
        self.enabled = True
        self.dirs = []

    def md_filter(self, text, **kwargs):
        md = markdown.Markdown(
            extensions=self.config['markdown_extensions'],
            extension_configs=self.config['mdx_configs'] or {}
        )
        return jinja2.Markup(md.convert(text))

    def on_env(self, env, config, files):
        self.config = config
        env.filters['markdown'] = self.md_filter
        return env
