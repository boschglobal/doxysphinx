from typing import Any

import lxml.etree as etree


def load_code_element(html_string: str) -> etree._Element:
    """loads a single pre or code element in an html snippet string.

    There has to be only one pre or code element!!
    """
    parser: Any = etree.HTMLParser()
    e = etree.fromstring(html_string, parser)
    result: Any = e.find(f".//pre")
    if result is None:
        result = e.find(f".//code")
    return result


def clean_html_string(html: str) -> str:
    """Removes whitespaces from html strings."""
    return html.replace("\n", "").replace("  ", "").replace("> ", ">").replace(" <", "<").strip()
