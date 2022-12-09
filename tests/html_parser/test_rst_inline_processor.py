import lxml.etree as etree
import pytest

from doxysphinx.html_parser import RstInlineProcessor

inline_rst_role_with_backticks = """
<div>
    Lorem ipsum pretext <code>:doc:`Home &lt;index&gt;`</code>, lorem ipsum posttext.
</div>
"""

inline_rst_role_with_apostrophe = """
<div>
    Lorem ipsum pretext <code>:doc:'Home &lt;index&gt;'</code>, lorem ipsum posttext.
</div>
"""

inline_rst_role_with_quote = """
<div>
    Lorem ipsum pretext <code>:doc:"Home &lt;index&gt;"</code>, lorem ipsum posttext.
</div>
"""

invalid_rst_role_1 = """
<div>
    Lorem ipsum pretext <code>.. admonition:: Hello There!</code>, lorem ipsum posttext.
</div>
"""

invalid_rst_role_2 = """
<div>
    Lorem ipsum pretext 
    <code>rst
    ..admonition:: this is rst

    rendered text
    </code>
</div>
"""

invalid_rst_role_3 = """
<div><code/></div>
"""

expected_rst_role = """
<div class="doxysphinx-inline-parent">
    Lorem ipsum pretext 
    <snippet type="rst:inline">:doc:`Home &lt;index&gt;`</snippet>
    , lorem ipsum posttext.
</div>
"""

inline_rst_domain_with_quote = """
<div>
    This is a link to a python class <code>:py:doxysphinx:"my_awesome_func(input: str)"</code>. Should work!
</div>
"""

expected_rst_domain = """
<div class="doxysphinx-inline-parent">
    This is a link to a python class 
    <snippet type="rst:inline">:py:doxysphinx:`my_awesome_func(input: str)`</snippet>
    . Should work!
</div>
"""


def _load_code_element(html_string: str) -> etree._Element:
    parser: Any = etree.HTMLParser()
    e = etree.fromstring(html_string, parser)
    result: Any = e.find(".//code")
    return result


def _clean_html_string(html: str):
    return html.replace("\n", "").replace("  ", "").replace("> ", ">").replace(" <", "<").strip()


@pytest.mark.parametrize(
    "input, expected",
    [
        pytest.param(inline_rst_role_with_backticks, expected_rst_role, id="inline_rst_role_with_backticks"),
        pytest.param(inline_rst_role_with_apostrophe, expected_rst_role, id="inline_rst_role_with_apostrophe"),
        pytest.param(inline_rst_role_with_quote, expected_rst_role, id="inline_rst_role_with_quote"),
        pytest.param(inline_rst_domain_with_quote, expected_rst_domain, id="inline_rst_domain_with_quote"),
    ],
)
def test_rst_inline_processor(input: str, expected: str):
    element = _load_code_element(input)

    proc = RstInlineProcessor()
    result = proc.try_process(element)
    assert result is True
    root_div = element.getparent()

    rendered_element = etree.tostring(root_div, encoding="unicode", pretty_print=True)
    a = _clean_html_string(rendered_element)
    b = _clean_html_string(expected)
    assert a == b


@pytest.mark.parametrize(
    "input, expected",
    [
        pytest.param(invalid_rst_role_1, invalid_rst_role_1, id="invalid_rst_role_1"),
        pytest.param(invalid_rst_role_2, invalid_rst_role_2, id="invalid_rst_role_1"),
        pytest.param(invalid_rst_role_3, invalid_rst_role_3, id="invalid_rst_role_1"),
    ],
)
def test_rst_inline_processor_doesnt_parse_invalid_data(input: str, expected: str):
    element = _load_code_element(input)

    proc = RstInlineProcessor()
    result = proc.try_process(element)
    assert result is False
    root_div = element.getparent()

    rendered_element = etree.tostring(root_div, encoding="unicode", pretty_print=True)
    a = _clean_html_string(rendered_element)
    b = _clean_html_string(expected)
    assert a == b
