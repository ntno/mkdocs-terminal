from jinja2 import pass_context as contextfilter
import mkdocs.utils.filters
MOCK_URL_PATH_PREFIX = "mocked_url_path/"
MOCK_MARKUP_INDICATOR = "MD_TO_HTML-%s-MD_TO_HTML"


@contextfilter
def mock_url_filter(context, value: str) -> str:
    return MOCK_URL_PATH_PREFIX + value


@contextfilter
def url_filter(context, value: str) -> str:
    return mkdocs.utils.filters.url_filter


@contextfilter
def mock_markup_filter(context, value: str) -> str:
    return MOCK_MARKUP_INDICATOR % value
