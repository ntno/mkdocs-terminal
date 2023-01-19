from jinja2 import pass_context as contextfilter
import mkdocs.utils.filters
MOCK_URL_PATH_PREFIX = "mocked_url_path/"
MOCK_MARKUP_INDICATOR = "MARKED"


@contextfilter
def mock_url_filter(context, value: str) -> str:
    return MOCK_URL_PATH_PREFIX + value


@contextfilter
def url_filter(context, value: str) -> str:
    return mkdocs.utils.filters.url_filter


@contextfilter
def mock_markup_filter(context, value: str) -> str:
    return MOCK_MARKUP_INDICATOR + value + MOCK_MARKUP_INDICATOR
