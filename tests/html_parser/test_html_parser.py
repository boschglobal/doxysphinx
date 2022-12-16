import re
from pathlib import Path
from typing import Any, Iterable, List, Tuple

import lxml.etree as etree
import pytest

from doxysphinx.html_parser import DoxygenHtmlParser, HtmlParser


def _read_data() -> List[Any]:
    results = []
    test_files = Path(__file__).parent / "test_files"
    for input_file in test_files.glob("*.input.html"):
        expected_name = Path(input_file.stem).stem
        expected_file = input_file.parent / (expected_name + ".expected.html")
        results.append((input_file, expected_file))
    return results


def ids_for(values: List[Any]) -> List[str]:
    results = []

    for v in values:
        first, second = v
        name = Path(first.stem).stem
        results.append(name)

    return results


DATA = _read_data()


@pytest.mark.parametrize("input, expected", DATA, ids=ids_for(DATA))
def test_html_parser_works_as_expected(input: Path, expected: Path):

    x = DoxygenHtmlParser(Path(__file__).parent)
    result = x.parse(input)

    # if the result has no tree (= no snippets found), we ensure that no expected file exists and vice versa
    if not expected.exists():
        assert result.tree == None
        return

    if result.tree == None:
        assert not expected.exists()
        return

    parsed_html = etree.tostring(
        result.tree,
        encoding="unicode",
    )

    # if there was a result and an expected file then we compare them...
    parsed_output = input.parent / (Path(input.stem).stem + ".parsed.html")
    parsed_output.write_text(parsed_html)

    expected_html = expected.read_text()

    assert parsed_html.strip() == expected_html.strip()
