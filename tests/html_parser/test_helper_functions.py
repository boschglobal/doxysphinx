import re
from typing import List

import pytest
from lxml.etree import HTMLParser, _Element, fromstring, tostring

from doxysphinx.html_parser import (
    _ensure_newline_after_element,
    _ensure_newline_before_element,
    _remove_doxygen_comment_prefixes,
    _try_parse_rst_block_content,
)

single_element_in_parent = """
<html>
    <body>
        <code></code>
    </body>
</html>
"""

element_with_siblings_before = """
<html>
    <body>
        <div id="1">First</div>
        <div id="2">Second</div>
        <code></code>
    </body>
</html>
"""

element_with_siblings_after = """
<html>
    <body>
        <code></code>
        <div id="1">First</div> 
        <div id="2">Second</div>
    </body>
</html>
"""

element_with_siblings_around = """
<html>
    <body>
        <div id="1">First</div>
        <div id="2">Second</div> 
        <code></code>
        <div id="3">Third</div>
        <div id="4">Forth</div>
    </body>
</html>
"""

element_with_text_before = """
<html>
    <body>
        Lorem ipsum dolor sit before
        <code></code>
    </body>
</html>
"""

element_with_text_after = """
<html>
    <body>
        <code></code>
        Lorem ipsum dolor sit after
    </body>
</html>
"""

element_with_text_around = """
<html>
    <body>
        Lorem ipsum dolor sit before
        <code></code>
        Lorem ipsum dolor sit after
    </body>
</html>
"""

element_with_newlines_before = """
<html>
    <body>




        <code></code>
    </body>
</html>
"""

element_with_newlines_after = """
<html>
    <body>
        <code></code>




    </body>
</html>
"""

element_with_newlines_around = """
<html>
    <body>
        
        

        <code></code>
        
        


    </body>
</html>
"""


def _build_test_set() -> List:
    input = [
        (single_element_in_parent, "single_element_in_parent"),
        (element_with_siblings_before, "element_with_siblings_before"),
        (element_with_siblings_after, "element_with_siblings_after"),
        (element_with_siblings_around, "element_with_siblings_around"),
        (element_with_text_before, "element_with_text_before"),
        (element_with_text_after, "element_with_text_after"),
        (element_with_text_around, "element_with_text_around"),
        (element_with_newlines_before, "element_with_newlines_before"),
        (element_with_newlines_after, "element_with_newlines_after"),
        (element_with_newlines_around, "element_with_newlines_around"),
    ]

    result = []
    for data, id in input:
        result.append(pytest.param(data, id=f"pretty_{id}"))
    for data, id in input:
        whitespaceless_data = data.replace("\n", "").replace("  ", "").replace("> ", ">").replace(" <", "<")
        result.append(pytest.param(whitespaceless_data, id=f"condensed_{id}"))
    return result


DEFAULT_TEST_SET = _build_test_set()


def _load_code_element(html_string: str) -> _Element:
    parser: Any = HTMLParser()
    e = fromstring(html_string, parser)
    result: Any = e.find(".//code")
    return result


def _count_newlines_until_non_whitespace(text: str) -> int:
    count: int = 0
    for i, v in enumerate(text):
        if v.isalnum():
            break
        if v == "\n":
            count = count + 1
    return count


@pytest.mark.parametrize(
    "test, expected",
    [
        ("", 0),
        ("fdgfdkgfjg \n gdfkgjfkgfdj \ngkfdjgfdkg\ndfgfdkgjf", 0),
        ("\n", 1),
        ("\n\n\n  fd  kjg  fgkjg\n\n", 3),
        ("     \n     \n            \t\t\t     \n<test>\n\n\n", 3),
    ],
)
def test_count_newlines_until_non_whitespace(test: str, expected: int):
    assert _count_newlines_until_non_whitespace(test) == expected


@pytest.mark.parametrize("html_string", DEFAULT_TEST_SET)
def test_ensure_newline_before_element(html_string: str):
    prefix, _ = html_string.split("<code>")
    newlines_before_processing = _count_newlines_until_non_whitespace(prefix[::-1])

    code_element = _load_code_element(html_string)

    _ensure_newline_before_element(code_element)

    root = code_element.getroottree().getroot()
    html_output = tostring(root, encoding="unicode")

    prefix, _ = html_output.split("<code/>")
    newlines_after_processing = _count_newlines_until_non_whitespace(prefix[::-1])

    assert (newlines_after_processing == newlines_before_processing + 1) or (
        newlines_after_processing == newlines_before_processing
    )
    assert newlines_after_processing >= 1


@pytest.mark.parametrize("html_string", DEFAULT_TEST_SET)
def test_ensure_newline_after_element(html_string: str):
    _, suffix = html_string.split("</code>")
    newlines_before_processing = _count_newlines_until_non_whitespace(suffix)

    code_element = _load_code_element(html_string)

    _ensure_newline_after_element(code_element)

    root = code_element.getroottree().getroot()
    html_output = tostring(root, encoding="unicode")

    _, suffix = html_output.split("<code/>")
    newlines_after_processing = _count_newlines_until_non_whitespace(suffix)

    assert (newlines_after_processing == newlines_before_processing + 1) or (
        newlines_after_processing == newlines_before_processing
    )
    assert newlines_after_processing >= 1


@pytest.mark.parametrize(
    "input, expected",
    [
        # main doxysphinx marker with some variants regarding whitespaces
        pytest.param("{rst}\nFIRST_LINE\nSECOND_LINE", "FIRST_LINE\nSECOND_LINE"),
        pytest.param("  {rst}\nFIRST_LINE\nSECOND_LINE", "FIRST_LINE\nSECOND_LINE"),
        pytest.param(" \n {rst}\nFIRST_LINE\nSECOND_LINE", "FIRST_LINE\nSECOND_LINE"),
        pytest.param("{rst}\nFIRST_LINE\nSECOND_LINE", "FIRST_LINE\nSECOND_LINE"),
        pytest.param("   {rst}\n   FIRST_LINE\n   SECOND_LINE", "FIRST_LINE\nSECOND_LINE"),
        # breathe compatibility markers
        pytest.param("embed:rst\nFIRST_LINE\nSECOND_LINE", "FIRST_LINE\nSECOND_LINE"),
        pytest.param("embed:rst:leading-slashes\nFIRST_LINE\nSECOND_LINE", "FIRST_LINE\nSECOND_LINE"),
        pytest.param("embed:rst:leading-asterisk\nFIRST_LINE\nSECOND_LINE", "FIRST_LINE\nSECOND_LINE"),
        # directive auto detection
        pytest.param(".. directive::\nFIRST_LINE\nSECOND_LINE", ".. directive::\nFIRST_LINE\nSECOND_LINE"),
        pytest.param(".. directive:: title\nFIRST_LINE\nSECOND_LINE", ".. directive:: title\nFIRST_LINE\nSECOND_LINE"),
        pytest.param(
            "   .. directive:: title\n      FIRST_LINE\n      SECOND_LINE",
            ".. directive:: title\n   FIRST_LINE\n   SECOND_LINE",
        ),
        pytest.param("*  .. directive::\n*  FIRST_LINE\n*  SECOND_LINE", ".. directive::\nFIRST_LINE\nSECOND_LINE"),
        # negative tests
        pytest.param("{rst} content that shouldn't be here\nFIRST_LINE\nSECOND_LINE", None),
        pytest.param("rst\nFIRST_LINE\nSECOND_LINE", None),
        pytest.param("FIRST_LINE\nSECOND_LINE", None),
        pytest.param("..directive::no\nWrong directive, missing space between dots", None),
        pytest.param("", None),
        pytest.param("{markdown}\n\njust a test", None),
    ],
)
def test_try_parse_rst_block_content(input, expected):
    assert _try_parse_rst_block_content(input) == expected
