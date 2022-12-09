import re

import pytest

from doxysphinx.utils.contexts import TimedContext

# SPEED TEST ONLY
# run with pytest -s to see the console output with the timings

SUBJECT = """*rst
* first
* second
* third

embed:rst
/// first
/// second
/// third

embed:rst
/// first
/// second
/// third

embed:rst
* first
* second
* third

embed:rst
 * first
 * second
 * third

embed:rst
//! first
//! second
//! third
"""

EXPECTED = """rst
 first
 second
 third

embed:rst
 first
 second
 third

embed:rst
 first
 second
 third

embed:rst
 first
 second
 third

embed:rst
 first
 second
 third

embed:rst
 first
 second
 third
"""


def _remove_doxygen_comment_markers_replace(text: str) -> str:
    """Removes doxygen comment prefixes from texts."""

    text = text.replace("\n *", "\n").replace("\n*", "\n")
    text = text.replace("\n///", "\n").replace("\n//!", "\n")
    return text


# 17 secs
def _remove_doxygen_comment_markers_arrays(text: str) -> str:
    """Removes doxygen comment prefixes from texts."""

    lines = text.split("\n")
    result = []
    for l in lines:
        clean = l.strip()
        if clean.startswith("*"):
            result.append(clean[1:])
        elif clean.startswith("///") or clean.startswith("//!"):
            result.append(clean[3:])
    return "\n".join(result)


comment_cleanup_regex = re.compile(r"^\s*(\*|\/\/\/|\/\/!)", re.MULTILINE)


def _remove_doxygen_comment_markers_regex_sub(text: str) -> str:
    """Removes doxygen comment prefixes from texts."""

    return comment_cleanup_regex.sub("", text)


@pytest.mark.parametrize(
    "function, input, expected",
    [
        # (_remove_doxygen_comment_markers_replace, SUBJECT, EXPECTED),
        (_remove_doxygen_comment_markers_regex_sub, SUBJECT, EXPECTED),
    ],
)
def test_functions_work_as_expected(function, input, expected):
    assert function(input) == expected


@pytest.mark.speed
def test_comment_cleaner_speed():
    count = 1000000

    # with TimedContext() as t1:
    #     for i in range(0, count):
    #         result = _remove_doxygen_comment_markers_replace(SUBJECT)
    #         assert result == EXPECTED
    # print(f"replace: {t1.elapsed_humanized()}")

    with TimedContext() as t2:
        for i in range(0, count):
            result = _remove_doxygen_comment_markers_regex_sub(SUBJECT)
            assert result == EXPECTED
    print(f"regex sub: {t2.elapsed_humanized()}")


## RESULTS: replace = 2 seconds
##          regex sub = 8 seconds
## so classic is way faster
## however as we need to get rid of the whitespace upfront we've got a problem

if __name__ == "__main__":
    test_comment_cleaner_speed()
