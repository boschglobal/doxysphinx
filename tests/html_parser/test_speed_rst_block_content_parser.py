import re
import sys
from pathlib import Path
from typing import Iterable

import pytest

from doxysphinx.utils.contexts import TimedContext

current_dir = str(Path(__file__).parent)
if current_dir not in sys.path:
    sys.path.append(current_dir)

from test_utils import load_code_element


def _supported_markers() -> Iterable[str]:
    # doxysphinx markers
    yield "rst"
    yield "restructuredtext"
    # breathe compatibility markers
    yield "embed:rst:leading-asterisk"
    yield "embed:rst:leading-slashes"
    yield "embed:rst"


def _parse_content_classic(text: str) -> Iterable[str]:

    normalized_text = text.strip()

    marker_checks = [(x, normalized_text.startswith(x)) for x in _supported_markers()]

    for marker, found in marker_checks:
        if not found:
            continue

        content = "\n" + normalized_text[len(marker) :]  # remove marker at the front

        content_lines = content.split("\n")[1:]  # split into lines ignoring the first \n (the "marker"-line)

        yield from content_lines
        break  # stop for loop when we have a match


_search_regex = re.compile(
    r"^(?P<marker>rst|restructuredtext|embed:rst(:leading-(asterisk|slashes))?)\s*\r?\n$", re.MULTILINE
)
_marker_regex = re.compile(r"^(rst|restructuredtext|embed:rst(:leading-(asterisk|slashes))?)\s*\r?\n", re.MULTILINE)


def _parse_content_regex(text: str) -> Iterable[str]:

    normalized_text = text.strip()

    if match := _search_regex.match(normalized_text):
        marker = match.group("marker")
        content = "\n" + normalized_text[len(marker) :]  # remove marker at the front

        content_lines = content.split("\n")[1:]  # split into lines ignoring the first \n (the "marker"-line)

        yield from content_lines


def _parse_content_new_regex(text: str) -> str:

    if match := _marker_regex.match(text):
        # remove marker line
        content = text[match.end() :]

        return content

    return ""


rst_block_with_breathe_leading_asterisk_marker = """
<div>
    <pre class="fragment">embed:rst:leading-asterisk
    .. need:: test
       :status: open

       This is the description
    </pre>
</div>
"""


@pytest.mark.speed
def test_speed():

    element = load_code_element(rst_block_with_breathe_leading_asterisk_marker)
    content = element.text
    count = 100000
    with TimedContext() as t1:
        for i in range(0, count):
            test = list(_parse_content_classic(content))
    print(f"classic implementation: {t1.elapsed()}")

    with TimedContext() as t2:
        for i in range(0, count):
            test = list(_parse_content_regex(content))
    print(f"regex implementation: {t2.elapsed()}")

    with TimedContext() as t3:
        for i in range(0, count):
            test = _parse_content_new_regex(content)
    print(f"regex new implementation: {t3.elapsed()}")


if __name__ == "__main__":
    test_speed()
