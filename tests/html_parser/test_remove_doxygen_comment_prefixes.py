import pytest

from doxysphinx.html_parser import _remove_doxygen_comment_prefixes

regression_input_1 = """
 .. admonition:: What you should see here

    This text should be in an admonition box. It was generated from a doxygen javadoc comment **without any special identation**.

 *Note that we had to add a space between the backslash and the verbatim command in the code because doxygen parsing will freak out if we add the command there...*

 .. code:: cpp

    /**
     \ verbatim embed:rst

      ...rst-content-here...

     \ endverbatim
     *\/"""


@pytest.mark.parametrize(
    "text, expected",
    [
        # comment styles test
        pytest.param("\n/// first\n/// second", "\n first\n second"),
        pytest.param("\n* first\n* second", "\n first\n second"),
        pytest.param("\n//! first\n//! second", "\n first\n second"),
        pytest.param("\n  /// first\n  /// second", "\n first\n second"),
        pytest.param("\n  *  first\n  * second", "\n  first\n second"),
        pytest.param("\n  //!  first\n  //!  second", "\n  first\n  second"),
        # mixed styles should take first one
        pytest.param("/// first\n/// second\n * third\n/// forth", " first\n second\n * third\n forth"),
        # test previous regressions
        pytest.param(regression_input_1, regression_input_1),
    ],
)
def test_remove_doxygen_comment_markers(text: str, expected: str):
    result = _remove_doxygen_comment_prefixes(text)
    assert result == expected
