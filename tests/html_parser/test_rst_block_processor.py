import re
from typing import Iterable

import lxml.etree as etree
import pytest

from doxysphinx.html_parser import RstBlockProcessor
from doxysphinx.utils.contexts import TimedContext

rst_block_with_doxysphinx_marker = """
<div>
    <pre class="fragment">{rst}
    *    .. need:: test
    *       :status: open
    *
    *       This is the description
    </pre>
</div>
"""

rst_block_with_doxysphinx_autodetect_directive = """
<div>
    <pre class="fragment">
    *    .. need:: test
    *       :status: open
    *
    *       This is the description
    </pre>
</div>
"""


rst_block_with_doxysphinx_marker_and_strange_comments = """
<div>
    <pre class="fragment">{rst}
       //!    .. need:: test
       //!       :status: open
       //!  
       //!       This is the description
    </pre>
</div>
"""

rst_block_with_breathe_general_marker = """
<div>
    <pre class="fragment">embed:rst
        *  .. need:: test
        *     :status: open
        *
        *     This is the description
    </pre>
</div>
"""

rst_block_with_breathe_leading_asterisk_marker = """
<div>
    <pre class="fragment">embed:rst:leading-asterisk
      *.. need:: test
      *   :status: open
      *
      *   This is the description
    </pre>
</div>
"""

rst_block_with_breathe_leading_slashes_marker = """
<div>
    <pre class="fragment">embed:rst:leading-slashes
        ///.. need:: test
        ///   :status: open
        ///
        ///   This is the description
    </pre>
</div>
"""

invalid_rst_block_without_any_marker = """
<div>
    <pre class="fragment">
    ..need: test
       :status: open

       This is the description
    </pre>
</div>
"""

invalid_rst_block_with_breathe_inline_rst_marker = """
<div>
    <pre class="fragment">embed:rst:inline
    .. need:: test
       :status: open

       This is the description
    </pre>
</div>
"""

expected_rst_block = """
<div>
    <snippet type="rst:block">
    .. need:: test
       :status: open

       This is the description
    </snippet>
</div>
"""


def _load_code_element(html_string: str) -> etree._Element:
    parser: Any = etree.HTMLParser()
    e = etree.fromstring(html_string, parser)
    result: Any = e.find(f".//pre")
    if result is None:
        result = e.find(f".//code")
    return result


def _clean_html_string(html: str):
    return html.replace("\n", "").replace("  ", "").replace("> ", ">").replace(" <", "<").strip()


@pytest.mark.parametrize(
    "input, expected",
    [
        pytest.param(rst_block_with_doxysphinx_marker, expected_rst_block, id="rst_block_with_doxysphinx_marker"),
        pytest.param(
            rst_block_with_doxysphinx_autodetect_directive,
            expected_rst_block,
            id="rst_block_with_doxysphinx_autodetect_directive",
        ),
        pytest.param(
            rst_block_with_doxysphinx_marker_and_strange_comments,
            expected_rst_block,
            id="rst_block_with_doxysphinx_marker_and_strange_comments",
        ),
        pytest.param(
            rst_block_with_breathe_general_marker, expected_rst_block, id="rst_block_with_breathe_general_marker"
        ),
        pytest.param(
            rst_block_with_breathe_leading_asterisk_marker,
            expected_rst_block,
            id="rst_block_with_breathe_leading_asterisk_marker",
        ),
        pytest.param(
            rst_block_with_breathe_leading_slashes_marker,
            expected_rst_block,
            id="rst_block_with_breathe_leading_slashes_marker",
        ),
    ],
)
def test_rst_block_processor_works_as_expected(input: str, expected: str):
    element = _load_code_element(input)

    proc = RstBlockProcessor()
    result = proc.try_process(element)
    assert result is True
    root_div = element.getparent()

    rendered_element = etree.tostring(root_div, encoding="unicode")
    a = _clean_html_string(rendered_element)
    b = _clean_html_string(expected)
    assert a == b


@pytest.mark.parametrize(
    "input, expected",
    [
        pytest.param(
            invalid_rst_block_without_any_marker,
            invalid_rst_block_without_any_marker,
            id="invalid_rst_block_without_any_marker",
        ),
        pytest.param(
            invalid_rst_block_with_breathe_inline_rst_marker,
            invalid_rst_block_with_breathe_inline_rst_marker,
            id="invalid_rst_block_with_breathe_inline_rst_marker",
        ),
    ],
)
def test_rst_block_processor_with_invalid_blocks_does_nothing(input: str, expected: str):
    element = _load_code_element(input)

    proc = RstBlockProcessor()
    result = proc.try_process(element)
    assert result is False
    root_div = element.getparent()

    rendered_element = etree.tostring(root_div, encoding="unicode", pretty_print=True)
    a = rendered_element.strip()
    b = expected.strip()
    assert a == b
