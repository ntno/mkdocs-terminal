from tidylib import tidy_fragment

def check_html(fragment):
    result = {}
    document, errors = tidy_fragment(fragment,
        options={'numeric-entities':1})
    result['errors']  = errors
    result['document'] = document
    return result
