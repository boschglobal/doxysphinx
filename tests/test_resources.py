# =====================================================================================
#  C O P Y R I G H T
# -------------------------------------------------------------------------------------
#  Copyright (c) 2026 by Umut Alisoglu. All rights reserved.
#
#  Author(s):
#  - Umut Alisoglu
# =====================================================================================

import pytest

from doxysphinx.resources import DoxygenResourceProvider
from doxysphinx.sphinx import SphinxHtmlBuilderDirectoryMapper


@pytest.mark.parametrize(
    "color",
    [
        "hsl(from #f8d1cc h s calc(l + -3))",
        "hsl(from var(--warning-color) h s calc(l + -3))",
        "hsl(from #f8d1cc h s l / 0.5)",
    ],
)
def test_provide_resources_preserves_relative_hsl(tmp_path, color):
    resource_root = tmp_path / "doxygen"
    resource_root.mkdir()
    source = resource_root / "doxygen.css"
    source.write_text(f"dl.warning .tt {{ background-color: {color}; }}", encoding="utf-8")
    mapper = SphinxHtmlBuilderDirectoryMapper(tmp_path, tmp_path / "output")
    provider = DoxygenResourceProvider(mapper)
    target = mapper.map(source)

    assert target in provider.provide_resources(resource_root)
    result = target.read_text(encoding="utf-8")
    assert ".doxygen-content dl.warning .tt {" in result
    expected_color = color.replace("hsl(", "HSL(", 1)
    assert "".join(expected_color.split()) in "".join(result.split())
    assert source.read_text(encoding="utf-8") == f"dl.warning .tt {{ background-color: {color}; }}"

    # Reusing the same input must keep the existing scoped stylesheet untouched.
    modified = target.stat().st_mtime_ns
    assert target not in provider.provide_resources(resource_root)
    assert target.stat().st_mtime_ns == modified


def test_provide_resources_keeps_classic_hsl_and_html_scope(tmp_path):
    resource_root = tmp_path / "doxygen"
    resource_root.mkdir()
    source = resource_root / "doxygen.css"
    source.write_text("html { --color: red; } p { color: hsl(120, 50%, 40%); }", encoding="utf-8")
    mapper = SphinxHtmlBuilderDirectoryMapper(tmp_path, tmp_path / "output")
    provider = DoxygenResourceProvider(mapper)

    provider.provide_resources(resource_root)
    result = mapper.map(source).read_text(encoding="utf-8")
    assert "html {" in result
    assert ".doxygen-content html {" not in result
    assert ".doxygen-content p {" in result
    assert "color: #339933;" in result
