from jinja2 import pass_context as contextfilter
from jinja2.utils import markupsafe
import markdown
import mkdocs.utils.filters
MOCK_URL_PATH_PREFIX = "mocked_url_path/"


@contextfilter
def mock_url_filter(context, value: str) -> str:
    return MOCK_URL_PATH_PREFIX + value


@contextfilter
def url_filter(context, value: str) -> str:
    return mkdocs.utils.filters.url_filter


@contextfilter
def mock_markdown_filter(context, value: str) -> str:
    md = markdown.Markdown(extensions=['meta'])
    return markupsafe.Markup(md.convert(value))
